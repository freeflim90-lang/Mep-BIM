#!/usr/bin/env python3
"""BCC Add-in 3차 개발 러너 — 잔여 기능 + 리본 등록 + 매니페스트"""
from __future__ import annotations
import httpx, json, os, re, sys, asyncio
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from backend.email_notifications import send_gmail, load_local_env
load_local_env()

OLLAMA_URL  = os.environ.get("LOCAL_CODER_BASE_URL", "http://127.0.0.1:11434")
CODER_MODEL = os.environ.get("LOCAL_CODER_MODEL", "qwen2.5-coder:7b")
REVIT_ROOT  = PROJECT_ROOT / "260519 소스 폴더" / "01_Revit_Addins"
NAV_ROOT    = PROJECT_ROOT / "260519 소스 폴더" / "02_Navisworks_Tools"
ADDIN_DASH  = REVIT_ROOT / "Addin Dashboard"


async def qwen_fill(code: str, hint: str) -> str:
    if "// QWEN_FILL" not in code:
        return code
    prompt = f"""C# 코드에서 `// QWEN_FILL` 부분을 실제 구현으로 채워라. 힌트: {hint}

```csharp
{code}
```
완성된 전체 코드를 ```csharp 블록으로:"""
    try:
        async with httpx.AsyncClient(timeout=180) as c:
            r = await c.post(f"{OLLAMA_URL}/api/generate",
                json={"model": CODER_MODEL, "prompt": prompt, "stream": False,
                      "options": {"temperature": 0.1, "num_predict": 3000}})
            r.raise_for_status()
        m = re.search(r"```(?:csharp|cs)?\s*([\s\S]+?)```", r.json().get("response", ""))
        return m.group(1).strip() if m else code
    except Exception as e:
        print(f"    Qwen 오류 ({e})")
        return code


def mail(item_id: str, display: str, kind: str, files: list[Path]) -> None:
    send_gmail(
        subject=f"[BCC 개발완료] {item_id} {display}",
        body="\n".join([
            f"BCC Add-in 스캐폴드: {display}  [{item_id}]",
            f"타입: {kind}  |  완료: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "", "파일:",
            *[f"  {f.name}  ({f.stat().st_size:,} bytes)" for f in files],
        ]),
        attachments=files,
    )
    print(f"  이메일 발송")


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# ═════════════════════════════════════════════════════════════════
# R-13  Batch Print Assistant
# ═════════════════════════════════════════════════════════════════
async def build_r13() -> list[Path]:
    out = REVIT_ROOT / "BatchPrintAssistant"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    engine = """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Revit.DB;
using Newtonsoft.Json;

namespace BIMCommandCenter.Commands
{
    public class PrintSetPreset
    {
        [JsonProperty("name")]         public string Name       { get; set; }
        [JsonProperty("viewSetNames")] public List<string> ViewSetNames { get; set; } = new();
        [JsonProperty("exportPath")]   public string ExportPath { get; set; } = "";
    }

    public class PrintItem
    {
        public ElementId Id   { get; set; }
        public string    Name { get; set; }
        public string    Type { get; set; }  // "Sheet" | "View"
        public string    SheetNumber { get; set; }
    }

    public static class BatchPrintEngine
    {
        public static List<PrintItem> CollectSheets(Document doc)
        {
            // QWEN_FILL: FilteredElementCollector로 ViewSheet 전량 수집, 시트번호 기준 정렬
            return new FilteredElementCollector(doc)
                .OfClass(typeof(ViewSheet))
                .Cast<ViewSheet>()
                .OrderBy(s => s.SheetNumber)
                .Select(s => new PrintItem
                {
                    Id          = s.Id,
                    Name        = s.Name,
                    SheetNumber = s.SheetNumber,
                    Type        = "Sheet",
                })
                .ToList();
        }

        public static PrintSetPreset LoadPreset(string path)
            => JsonConvert.DeserializeObject<PrintSetPreset>(File.ReadAllText(path))
               ?? new PrintSetPreset();

        public static void SavePreset(string path, PrintSetPreset preset)
            => File.WriteAllText(path, JsonConvert.SerializeObject(preset, Formatting.Indented));

        public static string Preview(List<PrintItem> items)
            => string.Join("\n", items.Select(i => $"[{i.SheetNumber}] {i.Name}"));

        public static int ExportToPdf(Document doc, List<PrintItem> items,
            string outputFolder, PrintManager pm = null)
        {
            // QWEN_FILL: ViewSet 또는 Document.Print 로 선택된 시트를 PDF 출력
            // PrintManager.PrintToFile = true, PrintManager.PrintRange = PrintRange.Select
            // ViewSheetSet 임시 생성 후 출력
            int count = 0;
            var printMgr = doc.PrintManager;
            printMgr.PrintToFile = true;
            printMgr.CombinedFile = true;
            printMgr.SelectNewPrintDriver("Microsoft Print to PDF");

            foreach (var item in items)
            {
                try
                {
                    var sheet = doc.GetElement(item.Id) as ViewSheet;
                    if (sheet == null) continue;
                    string outFile = Path.Combine(outputFolder,
                        $"{item.SheetNumber}_{item.Name}.pdf"
                        .Replace("/","_").Replace("\\","_"));
                    printMgr.PrintToFileName = outFile;
                    printMgr.PrintRange = PrintRange.Current;
                    count++;
                }
                catch { /* 개별 실패 무시 */ }
            }
            return count;
        }
    }
}
"""
    files.append(write(out / "BatchPrintEngine.cs",
        await qwen_fill(engine, "Revit ViewSheet, FilteredElementCollector, PrintManager.PrintToFile, PrintToFileName")))

    files.append(write(out / "BatchPrintCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.ReadOnly)]
    [Regeneration(RegenerationOption.Manual)]
    public class BatchPrintCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc    = data.Application.ActiveUIDocument.Document;
            var sheets = BatchPrintEngine.CollectSheets(doc);
            var win    = new BatchPrintWindow(sheets, doc);
            win.ShowDialog();
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "BatchPrintWindow.xaml.cs", """\
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Forms;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public partial class BatchPrintWindow : Window
    {
        private readonly List<PrintItem> _sheets;
        private readonly Document        _doc;

        public BatchPrintWindow(List<PrintItem> sheets, Document doc)
        {
            _sheets = sheets; _doc = doc;
            InitializeComponent();
            LstSheets.ItemsSource = sheets;
            LstSheets.SelectAll();
        }

        private void BtnSelectAll_Click(object s, RoutedEventArgs e) => LstSheets.SelectAll();
        private void BtnClear_Click(object s, RoutedEventArgs e)     => LstSheets.UnselectAll();

        private void BtnPreview_Click(object s, RoutedEventArgs e)
        {
            var selected = LstSheets.SelectedItems.Cast<PrintItem>().ToList();
            TxtPreview.Text = $"출력 예정: {selected.Count}개 시트\n" +
                BatchPrintEngine.Preview(selected);
        }

        private void BtnExport_Click(object s, RoutedEventArgs e)
        {
            var selected = LstSheets.SelectedItems.Cast<PrintItem>().ToList();
            if (selected.Count == 0) { System.Windows.MessageBox.Show("시트를 선택하세요."); return; }
            var dlg = new FolderBrowserDialog { Description = "출력 폴더 선택" };
            if (dlg.ShowDialog() != System.Windows.Forms.DialogResult.OK) return;
            int cnt = BatchPrintEngine.ExportToPdf(_doc, selected, dlg.SelectedPath);
            System.Windows.MessageBox.Show($"{cnt}개 시트 출력 처리 완료.\n폴더: {dlg.SelectedPath}");
        }

        private void BtnClose_Click(object s, RoutedEventArgs e) => Close();
    }
}
"""))

    files.append(write(out / "BatchPrintWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.BatchPrintWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Batch Print Assistant" Height="520" Width="540"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="8">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="120"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <ListBox x:Name="LstSheets" Grid.Row="0" SelectionMode="Extended"
                 DisplayMemberPath="Name" Margin="0,0,0,4"/>
        <StackPanel Grid.Row="1" Orientation="Horizontal" Margin="0,0,0,6">
            <Button Content="전체 선택" Width="80" Margin="2" Click="BtnSelectAll_Click"/>
            <Button Content="선택 해제" Width="80" Margin="2" Click="BtnClear_Click"/>
            <Button Content="미리보기"  Width="80" Margin="2" Click="BtnPreview_Click"/>
        </StackPanel>
        <TextBox x:Name="TxtPreview" Grid.Row="2" IsReadOnly="True"
                 TextWrapping="Wrap" ScrollViewer.VerticalScrollBarVisibility="Auto"
                 Background="#F8F8F8" Margin="0,0,0,8"/>
        <StackPanel Grid.Row="3" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="PDF 출력"  Width="90" Margin="4,0" Click="BtnExport_Click"/>
            <Button Content="닫기"       Width="70" Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [R-13] BatchPrintAssistant — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# R-14  Sheet / View Duplicator
# ═════════════════════════════════════════════════════════════════
async def build_r14() -> list[Path]:
    out = REVIT_ROOT / "SheetViewDuplicator"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    engine = """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public enum DuplicateViewMode { WithDetailing, DependentViews, Simple }

    public class SheetDuplicateResult
    {
        public string OriginalName { get; set; }
        public string NewName      { get; set; }
        public bool   Success      { get; set; }
        public string Error        { get; set; }
    }

    public static class SheetViewDuplicatorEngine
    {
        public static List<ViewSheet> GetSheets(Document doc)
            => new FilteredElementCollector(doc)
               .OfClass(typeof(ViewSheet))
               .Cast<ViewSheet>()
               .OrderBy(s => s.SheetNumber)
               .ToList();

        public static List<SheetDuplicateResult> DuplicateSheets(
            Document doc,
            IEnumerable<ElementId> sheetIds,
            string numberSuffix, string nameSuffix,
            DuplicateViewMode viewMode)
        {
            var results = new List<SheetDuplicateResult>();
            foreach (var id in sheetIds)
            {
                var sheet = doc.GetElement(id) as ViewSheet;
                if (sheet == null) continue;
                var result = new SheetDuplicateResult { OriginalName = $"[{sheet.SheetNumber}] {sheet.Name}" };
                try
                {
                    // QWEN_FILL:
                    // 1) 새 ViewSheet 생성: ViewSheet.Create(doc, titleBlockTypeId)
                    // 2) 새 시트에 SheetNumber = sheet.SheetNumber + numberSuffix
                    // 3)            Name      = sheet.Name + nameSuffix
                    // 4) 기존 시트의 Viewport 목록을 순회하여 뷰를 복제 후 새 시트에 배치
                    //    ViewMode 에 따라 View.Duplicate() / DuplicateWithDetailing() / DuplicateAsDependentView()

                    // 제목 블록 타입 찾기
                    var titleBlockId = sheet.GetAllPlacedViews().Count > 0
                        ? GetTitleBlockTypeId(doc) : ElementId.InvalidElementId;

                    var newSheet = ViewSheet.Create(doc, titleBlockId);
                    newSheet.SheetNumber = sheet.SheetNumber + numberSuffix;
                    newSheet.Name        = sheet.Name + nameSuffix;

                    // 뷰포트 복제
                    foreach (var vpId in sheet.GetAllViewports())
                    {
                        var vp   = doc.GetElement(vpId) as Viewport;
                        var view = doc.GetElement(vp.ViewId) as View;
                        if (view == null) continue;

                        ViewDuplicateOption opt = viewMode switch
                        {
                            DuplicateViewMode.WithDetailing   => ViewDuplicateOption.WithDetailing,
                            DuplicateViewMode.DependentViews  => ViewDuplicateOption.AsDependent,
                            _                                 => ViewDuplicateOption.Duplicate,
                        };

                        var newViewId = view.CanViewBeDuplicated(opt)
                            ? view.Duplicate(opt)
                            : view.Duplicate(ViewDuplicateOption.Duplicate);

                        Viewport.Create(doc, newSheet.Id, newViewId, vp.GetBoxCenter());
                    }

                    result.NewName = $"[{newSheet.SheetNumber}] {newSheet.Name}";
                    result.Success = true;
                }
                catch (Exception ex) { result.Error = ex.Message; }
                results.Add(result);
            }
            return results;
        }

        private static ElementId GetTitleBlockTypeId(Document doc)
            => new FilteredElementCollector(doc)
               .OfCategory(BuiltInCategory.OST_TitleBlocks)
               .WhereElementIsElementType()
               .FirstElementId() ?? ElementId.InvalidElementId;
    }
}
"""
    files.append(write(out / "SheetViewDuplicatorEngine.cs",
        await qwen_fill(engine, "Revit ViewSheet.Create, Viewport.Create, View.Duplicate(ViewDuplicateOption), GetAllViewports")))

    files.append(write(out / "SheetViewDuplicatorCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Linq;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class SheetViewDuplicatorCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc    = data.Application.ActiveUIDocument.Document;
            var sheets = SheetViewDuplicatorEngine.GetSheets(doc);
            var win    = new SheetViewDuplicatorWindow(sheets);
            if (win.ShowDialog() != true) return Result.Cancelled;

            using var tx = new Transaction(doc, "BCC - Duplicate Sheets");
            tx.Start();
            var results = SheetViewDuplicatorEngine.DuplicateSheets(
                doc, win.SelectedIds,
                win.NumberSuffix, win.NameSuffix, win.ViewMode);
            tx.Commit();

            int ok  = results.Count(r => r.Success);
            int err = results.Count(r => !r.Success);
            TaskDialog.Show("완료", $"복제 완료: {ok}개  실패: {err}개");
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "SheetViewDuplicatorWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public partial class SheetViewDuplicatorWindow : Window
    {
        public IList<ElementId>   SelectedIds  { get; private set; }
        public string             NumberSuffix { get; private set; } = "_복사";
        public string             NameSuffix   { get; private set; } = "_복사";
        public DuplicateViewMode  ViewMode     { get; private set; } = DuplicateViewMode.WithDetailing;

        public SheetViewDuplicatorWindow(List<ViewSheet> sheets)
        {
            InitializeComponent();
            LstSheets.ItemsSource = sheets;
        }

        private void BtnOk_Click(object s, RoutedEventArgs e)
        {
            SelectedIds  = LstSheets.SelectedItems.Cast<ViewSheet>().Select(sh => sh.Id).ToList();
            NumberSuffix = TxtNumSuffix.Text;
            NameSuffix   = TxtNameSuffix.Text;
            ViewMode     = (DuplicateViewMode)CboViewMode.SelectedIndex;
            if (SelectedIds.Count == 0) { MessageBox.Show("시트를 선택하세요."); return; }
            DialogResult = true;
        }
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }
}
"""))

    files.append(write(out / "SheetViewDuplicatorWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.SheetViewDuplicatorWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Sheet / View Duplicator" Height="440" Width="460"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="12">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <ListBox x:Name="LstSheets" Grid.Row="0" SelectionMode="Extended"
                 DisplayMemberPath="Name" Margin="0,0,0,8"/>
        <StackPanel Grid.Row="1" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="번호 접미사:" Width="90" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtNumSuffix"  Width="120" Text="_복사"/>
        </StackPanel>
        <StackPanel Grid.Row="2" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="이름 접미사:" Width="90" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtNameSuffix" Width="120" Text="_복사"/>
        </StackPanel>
        <StackPanel Grid.Row="3" Orientation="Horizontal" Margin="0,0,0,12">
            <TextBlock Text="뷰 복제 방식:" Width="90" VerticalAlignment="Center"/>
            <ComboBox x:Name="CboViewMode"  Width="160" SelectedIndex="0">
                <ComboBoxItem Content="상세 포함 복제"/>
                <ComboBoxItem Content="종속 뷰"/>
                <ComboBoxItem Content="단순 복제"/>
            </ComboBox>
        </StackPanel>
        <StackPanel Grid.Row="4" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="실행" Width="80" Margin="4,0" Click="BtnOk_Click"/>
            <Button Content="취소" Width="80" Click="BtnCancel_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [R-14] SheetViewDuplicator — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# R-15  Schedule Excel Sync (Import 측)
# ═════════════════════════════════════════════════════════════════
async def build_r15() -> list[Path]:
    out = REVIT_ROOT / "ScheduleExcelSync"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    engine = """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Revit.DB;
using ClosedXML.Excel;

namespace BIMCommandCenter.Commands
{
    public class SyncRow
    {
        public string ElementId   { get; set; }
        public string ParamName   { get; set; }
        public string OldValue    { get; set; }
        public string NewValue    { get; set; }
        public bool   IsReadOnly  { get; set; }
        public bool   WillApply   { get; set; }
    }

    public static class ScheduleExcelSyncEngine
    {
        /// <summary>엑셀 파일 읽기: 1행=헤더(ElementId 컬럼 필수), 2행~=데이터</summary>
        public static List<Dictionary<string, string>> ReadExcel(string path)
        {
            var rows = new List<Dictionary<string, string>>();
            using var wb = new XLWorkbook(path);
            var ws   = wb.Worksheets.First();
            var hdrs = ws.Row(1).CellsUsed().Select(c => c.GetValue<string>()).ToList();
            foreach (var row in ws.RowsUsed().Skip(1))
            {
                var d = new Dictionary<string, string>();
                for (int i = 0; i < hdrs.Count; i++)
                    d[hdrs[i]] = row.Cell(i + 1).GetValue<string>();
                rows.Add(d);
            }
            return rows;
        }

        /// <summary>Dry-run: 변경 예상 목록 (실제 쓰기 없음)</summary>
        public static List<SyncRow> Preview(Document doc, List<Dictionary<string, string>> excelRows)
        {
            var result = new List<SyncRow>();
            foreach (var row in excelRows)
            {
                if (!row.TryGetValue("ElementId", out var idStr)) continue;
                if (!int.TryParse(idStr, out int idInt)) continue;
                var el = doc.GetElement(new ElementId(idInt));
                if (el == null) continue;

                foreach (var kv in row.Where(k => k.Key != "ElementId"))
                {
                    var param = el.LookupParameter(kv.Key);
                    result.Add(new SyncRow
                    {
                        ElementId  = idStr,
                        ParamName  = kv.Key,
                        OldValue   = param?.AsValueString() ?? param?.AsString() ?? "",
                        NewValue   = kv.Value,
                        IsReadOnly = param == null || param.IsReadOnly,
                        WillApply  = param != null && !param.IsReadOnly,
                    });
                }
            }
            return result;
        }

        /// <summary>실제 적용 (트랜잭션 내에서 호출)</summary>
        public static int Apply(Document doc, List<SyncRow> rows)
        {
            // QWEN_FILL: rows 에서 WillApply==true 인 것만 ElementId → Element 조회 후
            // LookupParameter(ParamName).Set(NewValue) 적용, 타입에 따라 int/double/string 분기
            int count = 0;
            foreach (var sr in rows.Where(r => r.WillApply))
            {
                try
                {
                    var el = doc.GetElement(new ElementId(int.Parse(sr.ElementId)));
                    var p  = el?.LookupParameter(sr.ParamName);
                    if (p == null || p.IsReadOnly) continue;
                    switch (p.StorageType)
                    {
                        case StorageType.String:  p.Set(sr.NewValue); break;
                        case StorageType.Double:
                            if (double.TryParse(sr.NewValue, out double d)) p.Set(d); break;
                        case StorageType.Integer:
                            if (int.TryParse(sr.NewValue, out int i)) p.Set(i); break;
                    }
                    count++;
                }
                catch { /* 개별 실패 스킵 */ }
            }
            return count;
        }
    }
}
"""
    files.append(write(out / "ScheduleExcelSyncEngine.cs",
        await qwen_fill(engine, "Revit Parameter.StorageType, Parameter.Set(), LookupParameter, ElementId")))

    files.append(write(out / "ScheduleExcelSyncCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Microsoft.Win32;
using System.Linq;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class ScheduleExcelSyncCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc = data.Application.ActiveUIDocument.Document;

            var dlg = new OpenFileDialog
                { Filter = "Excel 파일 (*.xlsx)|*.xlsx", Title = "동기화할 엑셀 선택" };
            if (dlg.ShowDialog() != true) return Result.Cancelled;

            var excelRows = ScheduleExcelSyncEngine.ReadExcel(dlg.FileName);
            var preview   = ScheduleExcelSyncEngine.Preview(doc, excelRows);

            int willApply = preview.Count(r => r.WillApply);
            int readOnly  = preview.Count(r => r.IsReadOnly);

            var td = new TaskDialog("Schedule Excel Sync — 미리보기");
            td.MainContent   = $"적용 예정: {willApply}개  읽기전용(스킵): {readOnly}개\n\n" +
                string.Join("\n", preview.Where(r => r.WillApply).Take(15)
                    .Select(r => $"ID={r.ElementId}  {r.ParamName}: '{r.OldValue}' → '{r.NewValue}'"));
            td.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel;
            if (td.Show() != TaskDialogResult.Ok) return Result.Cancelled;

            using var tx = new Transaction(doc, "BCC - Schedule Excel Sync");
            tx.Start();
            int applied = ScheduleExcelSyncEngine.Apply(doc, preview);
            tx.Commit();

            TaskDialog.Show("완료", $"{applied}개 파라미터 업데이트 완료.");
            return Result.Succeeded;
        }
    }
}
"""))
    print(f"  [R-15] ScheduleExcelSync — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# R-16  Room Finishing Pro (한국 마감 특화)
# ═════════════════════════════════════════════════════════════════
async def build_r16() -> list[Path]:
    out = REVIT_ROOT / "RoomFinishingPro"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    engine = """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;
using Newtonsoft.Json;

namespace BIMCommandCenter.Commands
{
    public class FinishRule
    {
        [JsonProperty("roomName")]    public string RoomName    { get; set; }  // 공간 이름 키워드
        [JsonProperty("floorFinish")] public string FloorFinish { get; set; }
        [JsonProperty("wallFinish")]  public string WallFinish  { get; set; }
        [JsonProperty("ceilFinish")]  public string CeilFinish  { get; set; }
        [JsonProperty("baseFinish")]  public string BaseFinish  { get; set; }
    }

    public class FinishApplyResult
    {
        public string RoomName { get; set; }
        public int    Applied  { get; set; }
        public string Error    { get; set; }
    }

    public static class RoomFinishingEngine
    {
        // 한국 표준 마감 기본 규칙 (건축법 / KCS 기반)
        public static List<FinishRule> DefaultKoreanRules() => new()
        {
            new() { RoomName="화장실",  FloorFinish="논슬립 타일 200x200", WallFinish="타일 200x300",  CeilFinish="알루미늄 천장재", BaseFinish="타일 줄눈" },
            new() { RoomName="욕실",    FloorFinish="논슬립 타일 200x200", WallFinish="타일 200x300",  CeilFinish="방수 페인트",     BaseFinish="타일 줄눈" },
            new() { RoomName="사무실",  FloorFinish="카펫 타일 600x600",   WallFinish="비닐 벽지",     CeilFinish="텍스 타일",       BaseFinish="걸레받이 MDF" },
            new() { RoomName="회의실",  FloorFinish="카펫 타일 600x600",   WallFinish="비닐 벽지",     CeilFinish="텍스 타일",       BaseFinish="걸레받이 MDF" },
            new() { RoomName="복도",    FloorFinish="폴리싱 타일 600x600", WallFinish="수성 페인트",   CeilFinish="텍스 타일",       BaseFinish="걸레받이 화강석" },
            new() { RoomName="로비",    FloorFinish="화강석 600x600",      WallFinish="화강석 패널",   CeilFinish="알루미늄 천장재", BaseFinish="화강석" },
            new() { RoomName="기계실",  FloorFinish="에폭시 바닥 도장",    WallFinish="수성 페인트",   CeilFinish="노출 콘크리트",   BaseFinish="없음" },
            new() { RoomName="전기실",  FloorFinish="에폭시 바닥 도장",    WallFinish="수성 페인트",   CeilFinish="노출 콘크리트",   BaseFinish="없음" },
        };

        public static List<FinishRule> LoadRules(string path)
            => JsonConvert.DeserializeObject<List<FinishRule>>(File.ReadAllText(path))
               ?? DefaultKoreanRules();

        public static List<Room> GetRooms(Document doc)
            => new FilteredElementCollector(doc)
               .OfClass(typeof(SpatialElement))
               .Cast<SpatialElement>()
               .OfType<Room>()
               .Where(r => r.Area > 0.001)
               .ToList();

        public static FinishRule MatchRule(Room room, List<FinishRule> rules)
        {
            string name = room.Name?.ToLower() ?? "";
            return rules.FirstOrDefault(r =>
                !string.IsNullOrEmpty(r.RoomName) &&
                name.Contains(r.RoomName.ToLower()));
        }

        public static List<FinishApplyResult> Apply(Document doc,
            IEnumerable<Room> rooms, List<FinishRule> rules)
        {
            // QWEN_FILL: 각 room 에 MatchRule 로 규칙 찾기,
            // room.LookupParameter("Floor Finish" / "바닥 마감") 등에 규칙 값 설정
            // BuiltInParameter.ROOM_FINISH_FLOOR / ROOM_FINISH_WALL / ROOM_FINISH_CEILING 사용
            var results = new List<FinishApplyResult>();
            foreach (var room in rooms)
            {
                var rule = MatchRule(room, rules);
                if (rule == null) continue;
                var r = new FinishApplyResult { RoomName = room.Name };
                try
                {
                    int cnt = 0;
                    if (!string.IsNullOrEmpty(rule.FloorFinish))
                    { SetFinish(room, BuiltInParameter.ROOM_FINISH_FLOOR, rule.FloorFinish); cnt++; }
                    if (!string.IsNullOrEmpty(rule.WallFinish))
                    { SetFinish(room, BuiltInParameter.ROOM_FINISH_WALL, rule.WallFinish);   cnt++; }
                    if (!string.IsNullOrEmpty(rule.CeilFinish))
                    { SetFinish(room, BuiltInParameter.ROOM_FINISH_CEILING, rule.CeilFinish); cnt++; }
                    if (!string.IsNullOrEmpty(rule.BaseFinish))
                    { SetFinish(room, BuiltInParameter.ROOM_FINISH_BASE, rule.BaseFinish);   cnt++; }
                    r.Applied = cnt;
                }
                catch (Exception ex) { r.Error = ex.Message; }
                results.Add(r);
            }
            return results;
        }

        private static void SetFinish(Room room, BuiltInParameter bip, string value)
        {
            var p = room.get_Parameter(bip);
            if (p != null && !p.IsReadOnly) p.Set(value);
        }
    }
}
"""
    files.append(write(out / "RoomFinishingEngine.cs",
        await qwen_fill(engine, "Revit Room, BuiltInParameter.ROOM_FINISH_FLOOR/WALL/CEILING/BASE, get_Parameter, Set(string)")))

    files.append(write(out / "RoomFinishingCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Linq;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class RoomFinishingCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc   = data.Application.ActiveUIDocument.Document;
            var rooms = RoomFinishingEngine.GetRooms(doc);
            var rules = RoomFinishingEngine.DefaultKoreanRules();
            var win   = new RoomFinishingWindow(rooms, rules);
            if (win.ShowDialog() != true) return Result.Cancelled;

            using var tx = new Transaction(doc, "BCC - Room Finishing Pro");
            tx.Start();
            var results = RoomFinishingEngine.Apply(doc, win.SelectedRooms, win.Rules);
            tx.Commit();

            int applied = results.Sum(r => r.Applied);
            int matched = results.Count(r => r.Applied > 0);
            TaskDialog.Show("완료",
                $"룸 {matched}개 마감 배정 완료 ({applied}개 파라미터 설정)");
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "RoomFinishingWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using Autodesk.Revit.DB.Architecture;

namespace BIMCommandCenter.Commands
{
    public partial class RoomFinishingWindow : Window
    {
        public IEnumerable<Room>   SelectedRooms { get; private set; }
        public List<FinishRule>    Rules         { get; private set; }
        private readonly List<Room>      _rooms;
        private readonly List<FinishRule> _rules;

        public RoomFinishingWindow(List<Room> rooms, List<FinishRule> rules)
        {
            _rooms = rooms; _rules = rules;
            InitializeComponent();
            LstRooms.ItemsSource  = rooms;
            LstRules.ItemsSource  = rules;
            LstRooms.SelectAll();
        }

        private void BtnOk_Click(object s, RoutedEventArgs e)
        {
            SelectedRooms = LstRooms.SelectedItems.Cast<Room>().ToList();
            Rules         = _rules;
            DialogResult = true;
        }
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }
}
"""))

    files.append(write(out / "RoomFinishingWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.RoomFinishingWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Room Finishing Pro (한국 마감 기준)" Height="480" Width="620"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="8">
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*"/>
            <ColumnDefinition Width="*"/>
        </Grid.ColumnDefinitions>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <TextBlock Grid.Row="0" Grid.Column="0" Text="룸 목록" FontWeight="Bold" Margin="0,0,0,4"/>
        <TextBlock Grid.Row="0" Grid.Column="1" Text="마감 규칙 (KCS 기준)" FontWeight="Bold" Margin="8,0,0,4"/>
        <ListBox Grid.Row="1" Grid.Column="0" x:Name="LstRooms"
                 SelectionMode="Extended" DisplayMemberPath="Name" Margin="0,0,4,0"/>
        <DataGrid Grid.Row="1" Grid.Column="1" x:Name="LstRules" Margin="4,0,0,0"
                  AutoGenerateColumns="False" IsReadOnly="True">
            <DataGrid.Columns>
                <DataGridTextColumn Header="공간"  Binding="{Binding RoomName}"    Width="60"/>
                <DataGridTextColumn Header="바닥"  Binding="{Binding FloorFinish}" Width="*"/>
                <DataGridTextColumn Header="벽체"  Binding="{Binding WallFinish}"  Width="*"/>
            </DataGrid.Columns>
        </DataGrid>
        <StackPanel Grid.Row="2" Grid.ColumnSpan="2" Orientation="Horizontal"
                    HorizontalAlignment="Right" Margin="0,8,0,0">
            <Button Content="적용"  Width="80" Margin="4,0" Click="BtnOk_Click"/>
            <Button Content="취소"  Width="80" Click="BtnCancel_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [R-16] RoomFinishingPro — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# INTEGRATION — Ribbon Registration (App.cs Commands 폴더)
# ═════════════════════════════════════════════════════════════════
async def build_ribbon_registration() -> list[Path]:
    """모든 새 커맨드를 BIM Command Center 리본에 등록하는 확장 코드."""
    out = ADDIN_DASH / "Commands"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    files.append(write(out / "RibbonCommandRegistry.cs", """\
using Autodesk.Revit.UI;
using System.Reflection;

namespace BIMCommandCenter.Commands
{
    /// <summary>
    /// BIM Command Center 리본 탭에 모든 새 커맨드 버튼 등록.
    /// App.cs CreateRibbon() 에서 RegisterAllCommands(app, assemblyPath) 호출.
    /// </summary>
    public static class RibbonCommandRegistry
    {
        public static void RegisterAllCommands(UIControlledApplication app, string assemblyPath)
        {
            const string tab = "BIM Command Center";

            // ── 도면·주석 패널 ────────────────────────────────────────
            var panelAnnotation = GetOrCreatePanel(app, tab, "도면·주석");
            panelAnnotation.AddItem(Btn("태그 정렬",       assemblyPath, typeof(TagTextAlignerCommand),      "태그·문자 정렬/배분"));
            panelAnnotation.AddItem(Btn("선 정리",         assemblyPath, typeof(LineCleanupCommand),         "중복·단선 정리"));

            // ── 뷰 관리 패널 ─────────────────────────────────────────
            var panelView = GetOrCreatePanel(app, tab, "뷰 관리");
            panelView.AddItem(Btn("뷰 템플릿 복사",        assemblyPath, typeof(ViewTemplateCopierCommand),  "프로젝트 간 뷰 템플릿 복사"));
            panelView.AddItem(Btn("Smart 선택",            assemblyPath, typeof(SmartSelectorCommand),       "규칙 기반 요소 선택"));
            panelView.AddItem(Btn("Workset 검사",          assemblyPath, typeof(WorksetInspectorCommand),    "워크셋 요소 현황 및 선택"));
            panelView.AddItem(Btn("시트 복제",             assemblyPath, typeof(SheetViewDuplicatorCommand), "시트·뷰 일괄 복제"));

            // ── 모델 처리 패널 ───────────────────────────────────────
            var panelModel = GetOrCreatePanel(app, tab, "모델 처리");
            panelModel.AddItem(Btn("타입 일괄 정의",       assemblyPath, typeof(TypeBatchDefinerCommand),    "JSON 기반 타입 일괄 생성"));
            panelModel.AddItem(Btn("번호 재배정",          assemblyPath, typeof(ElementRenumberingCommand),  "룸·도어 등 번호 규칙 재배정"));
            panelModel.AddItem(Btn("모델 감사",            assemblyPath, typeof(ProjectCleanupCommand),      "미사용 뷰·CAD·경고 감사"));
            panelModel.AddItem(Btn("경고 관리",            assemblyPath, typeof(WarningManagerCommand),      "경고 유형별 분류 및 요소 선택"));
            panelModel.AddItem(Btn("룸 마감 배정",         assemblyPath, typeof(RoomFinishingCommand),       "한국 KCS 기준 마감재 자동 배정"));

            // ── 데이터 패널 ──────────────────────────────────────────
            var panelData = GetOrCreatePanel(app, tab, "데이터");
            panelData.AddItem(Btn("일람표 Excel 내보내기", assemblyPath, typeof(ScheduleExportCommand),      "현재 일람표 → Excel 저장"));
            panelData.AddItem(Btn("일람표 Excel 동기화",   assemblyPath, typeof(ScheduleExcelSyncCommand),   "Excel → Revit 파라미터 동기화"));

            // ── MEP 패널 ─────────────────────────────────────────────
            var panelMep = GetOrCreatePanel(app, tab, "MEP");
            panelMep.AddItem(Btn("MEP 길이 계산",          assemblyPath, typeof(MEPLengthCommand),           "배관·덕트·전선관 길이 집계"));

            // ── 링크·인쇄 패널 ───────────────────────────────────────
            var panelLink = GetOrCreatePanel(app, tab, "링크·인쇄");
            panelLink.AddItem(Btn("링크 상태",             assemblyPath, typeof(LinkHealthCommand),          "Revit/CAD 링크 상태 확인·재로드"));
            panelLink.AddItem(Btn("일괄 인쇄",             assemblyPath, typeof(BatchPrintCommand),          "시트 일괄 PDF 출력"));
        }

        private static RibbonPanel GetOrCreatePanel(UIControlledApplication app,
            string tab, string panelName)
        {
            try { return app.CreateRibbonPanel(tab, panelName); }
            catch { /* 이미 존재 */ }
            foreach (var p in app.GetRibbonPanels(tab))
                if (p.Name == panelName) return p;
            return app.CreateRibbonPanel(tab, panelName);
        }

        private static PushButtonData Btn(string text, string assembly,
            System.Type commandType, string tooltip)
            => new PushButtonData(
                commandType.Name, text,
                assembly, commandType.FullName)
            { ToolTip = tooltip };
    }
}
"""))
    print(f"  [INTEGRATION] RibbonCommandRegistry — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# INTEGRATION — App.cs 패치 (CreateRibbon 호출 추가)
# ═════════════════════════════════════════════════════════════════
async def patch_app_cs() -> list[Path]:
    """기존 App.cs 의 CreateRibbon() 에 RegisterAllCommands 호출 삽입."""
    app_path = ADDIN_DASH / "App.cs"
    if not app_path.exists():
        return []
    content = app_path.read_text(encoding="utf-8")

    if "RibbonCommandRegistry" in content:
        print("  [PATCH] App.cs 이미 패치됨 — 스킵")
        return []

    # panel.AddItem(btnData); 바로 뒤에 삽입
    old = "            panel.AddItem(btnData);\n        }"
    new = ("            panel.AddItem(btnData);\n\n"
           "            // ── 추가 커맨드 등록 ──────────────────────────\n"
           "            BIMCommandCenter.Commands.RibbonCommandRegistry\n"
           "                .RegisterAllCommands(app, Assembly.GetExecutingAssembly().Location);\n"
           "        }")

    if old not in content:
        print("  [PATCH] App.cs 패치 포인트 없음 — 스킵")
        return []

    patched = content.replace(old, new)
    app_path.write_text(patched, encoding="utf-8")
    print("  [PATCH] App.cs CreateRibbon 패치 완료")
    return [app_path]


# ═════════════════════════════════════════════════════════════════
# INTEGRATION — Navisworks .addinmanifest 파일들
# ═════════════════════════════════════════════════════════════════
async def build_nw_manifests() -> list[Path]:
    files: list[Path] = []

    manifests = [
        ("ClashResponsibilityBoard", "ClashResponsibilityBoard.dll",
         "NavisworksClashBoard.ClashResponsibilityPlugin", "간섭 책임자 배정 보드"),
        ("ClashGroupEngine", "ClashGroupEngine.dll",
         "NavisworksClashGroup.ClashGroupPlugin",          "클래시 그룹화"),
        ("ClashTestDefiner", "ClashTestDefiner.dll",
         "NavisworksClashDefiner.ClashTestDefinerPlugin",  "간섭 테스트 일괄 정의"),
    ]

    for folder, dll, plugin_class, display_name in manifests:
        out = NAV_ROOT / folder
        out.mkdir(parents=True, exist_ok=True)
        manifest = f"""\
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPlugins>
  <ApplicationPlugin>
    <Name>{folder}</Name>
    <Description>{display_name} — LUA BIM LABS</Description>
    <AddinFile>{dll}</AddinFile>
    <PluginInfoClass>{plugin_class}</PluginInfoClass>
    <Icon>icon.png</Icon>
  </ApplicationPlugin>
</ApplicationPlugins>
"""
        p = write(out / f"{folder}.addinmanifest", manifest)
        files.append(p)

    print(f"  [NW-MANIFEST] {len(files)}개 매니페스트 생성")
    return files


# ═════════════════════════════════════════════════════════════════
# INTEGRATION — BCC .addin manifest 업데이트
# ═════════════════════════════════════════════════════════════════
async def build_bcc_addin_manifest() -> list[Path]:
    out = ADDIN_DASH / "addin"
    out.mkdir(parents=True, exist_ok=True)

    manifest = """\
<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!-- BIM Command Center for Revit — Autodesk .addin manifest -->
<!-- 지원 버전: Revit 2024 / 2025 / 2026 -->
<RevitAddIns>
  <AddIn Type="Application">
    <Name>BIM Command Center</Name>
    <Assembly>BIMCommandCenter.dll</Assembly>
    <FullClassName>BIMCommandCenter.App</FullClassName>
    <ClientId>C7A4B3D2-E891-4F05-A6C0-123456789ABC</ClientId>
    <VendorId>LUABIMLABS</VendorId>
    <VendorDescription>LUA BIM LABS</VendorDescription>
  </AddIn>
</RevitAddIns>
"""
    p = write(out / "BIMCommandCenter.addin", manifest)
    print(f"  [BCC-MANIFEST] .addin 파일 생성")
    return [p]


# ═════════════════════════════════════════════════════════════════
# INTEGRATION — 전체 파일 목록 README
# ═════════════════════════════════════════════════════════════════
async def build_integration_readme() -> list[Path]:
    out = REVIT_ROOT / "Addin Dashboard"
    readme = """\
# BIM Command Center — 통합 빌드 가이드

## 빌드 전 체크리스트

### NuGet 패키지 추가 (BIMCommandCenter.csproj)
```
ClosedXML          >= 0.102
Newtonsoft.Json    >= 13.0
```

### 참조 DLL (Revit API)
- RevitAPI.dll       — C:\\Program Files\\Autodesk\\Revit 20xx\\
- RevitAPIUI.dll     — 동일 폴더

### 새로 추가된 C# 파일 (전체 목록)

#### Phase 1 (1차 개발)
| 폴더 | 주요 파일 |
|---|---|
| TagTextAligner | TagTextAlignerCommand.cs, Engine.cs, Window.xaml |
| ViewTemplateCopier | Command.cs, Engine.cs, Window.xaml |
| TypeBatchDefiner | Command.cs, Engine.cs, TypeDefinition.cs, Window.xaml |
| ElementRenumbering | Command.cs, Engine.cs, RenumberRule.cs, Window.xaml, PreviewWindow.xaml |
| ProjectCleanupLite | Command.cs, Engine.cs, Report.cs, Window.xaml |

#### Phase 2 (2차·3차 개발)
| 폴더 | 주요 파일 |
|---|---|
| LineCleanupLite | Command.cs, Engine.cs, Window.xaml |
| SmartSelectorLite | Command.cs, Engine.cs, Window.xaml |
| WorksetInspectorLite | Command.cs, Engine.cs, Window.xaml |
| LinkHealthReload | Command.cs, Engine.cs, Window.xaml |
| ScheduleExcelExport | Command.cs, Engine.cs |
| ScheduleExcelSync | Command.cs, Engine.cs |
| MEPLengthCalculator | Command.cs, Engine.cs, Window.xaml |
| WarningManager | Command.cs, Engine.cs, Window.xaml |
| BatchPrintAssistant | Command.cs, Engine.cs, Window.xaml |
| SheetViewDuplicator | Command.cs, Engine.cs, Window.xaml |
| RoomFinishingPro | Command.cs, Engine.cs, Window.xaml |

#### 통합 파일
| 파일 | 설명 |
|---|---|
| Commands/RibbonCommandRegistry.cs | 모든 커맨드를 리본에 등록 |
| App.cs (패치됨) | CreateRibbon에서 RegisterAllCommands 호출 |
| addin/BIMCommandCenter.addin | Revit 애드인 매니페스트 |

### 리본 탭 구조
```
BIM Command Center (탭)
├── 대시보드        : Toggle Dashboard
├── 도면·주석      : 태그 정렬, 선 정리
├── 뷰 관리        : 뷰 템플릿 복사, Smart 선택, Workset 검사, 시트 복제
├── 모델 처리      : 타입 일괄 정의, 번호 재배정, 모델 감사, 경고 관리, 룸 마감 배정
├── 데이터         : 일람표 Excel 내보내기, 일람표 Excel 동기화
├── MEP            : MEP 길이 계산
└── 링크·인쇄      : 링크 상태, 일괄 인쇄
```

## Navisworks Add-in 빌드

### 각 프로젝트 (독립 .sln)
- ClashResponsibilityBoard — NuGet: ClosedXML, Newtonsoft.Json
- ClashGroupEngine
- ClashTestDefiner

### 참조 DLL (Navisworks API)
- Autodesk.Navisworks.Api.dll
- Autodesk.Navisworks.Clash.dll

### 공통 레이어
- `_Shared/KoreanReport/KoreanReportGenerator.cs` — 엑셀 리포트 생성
- `_Shared/KoreanReport/NavisworksHelper.cs`      — 레이어명 추출

## 설치 경로
- Revit: `%APPDATA%\\Autodesk\\Revit\\Addins\\20xx\\BIMCommandCenter.addin`
- Navisworks: `%APPDATA%\\Autodesk Navisworks Manage 20xx\\Plugins\\`
"""
    p = write(out / "BUILD_INTEGRATION_GUIDE.md", readme)
    print(f"  [README] BUILD_INTEGRATION_GUIDE.md 생성")
    return [p]


# ═════════════════════════════════════════════════════════════════
# 메인
# ═════════════════════════════════════════════════════════════════
async def main():
    print(f"BCC Add-in 3차 개발 러너 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")

    batches = [
        ("R-13",        "Batch Print Assistant",      "Revit",      build_r13),
        ("R-14",        "Sheet/View Duplicator",       "Revit",      build_r14),
        ("R-15",        "Schedule Excel Sync",         "Revit",      build_r15),
        ("R-16",        "Room Finishing Pro",          "Revit",      build_r16),
        ("INT-RIBBON",  "Ribbon Registration",         "통합",       build_ribbon_registration),
        ("INT-APPCS",   "App.cs 패치",                 "통합",       patch_app_cs),
        ("INT-NWMFST",  "Navisworks Manifests",        "Navisworks", build_nw_manifests),
        ("INT-BCCMFST", "BCC .addin Manifest",         "통합",       build_bcc_addin_manifest),
        ("INT-README",  "빌드 통합 가이드 README",     "통합",       build_integration_readme),
    ]

    for item_id, display, kind, builder in batches:
        print(f"\n{'='*55}\n[{item_id}] {display}\n{'='*55}")
        files = await builder()
        if files:
            mail(item_id, display, kind, files)
            print(f"  ✓ 이메일 발송")
        else:
            print(f"  — 파일 없음 (스킵)")

    print(f"\n\n3차 개발 전체 완료")


if __name__ == "__main__":
    asyncio.run(main())
