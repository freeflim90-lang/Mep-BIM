#!/usr/bin/env python3
"""BCC Add-in 2차 개발 러너 — 누락 UI + Phase 2 + 신규 아이템"""
from __future__ import annotations
import httpx, json, os, re, sys, asyncio
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from backend.email_notifications import send_gmail, load_local_env
from scripts.addin_dev_paths import addin_dev_source_root, require_addin_dev_source_root
load_local_env()

OLLAMA_URL  = os.environ.get("LOCAL_CODER_BASE_URL", "http://127.0.0.1:11434")
CODER_MODEL = os.environ.get("LOCAL_CODER_MODEL", "qwen2.5-coder:7b")
DEV_SOURCE_ROOT = addin_dev_source_root() or Path("__missing_BCC_ADDIN_DEV_SOURCE_ROOT__")
REVIT_ROOT = DEV_SOURCE_ROOT / "01_Revit_Addins"
NAV_ROOT = DEV_SOURCE_ROOT / "02_Navisworks_Tools"


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
    result = send_gmail(
        subject=f"[BCC 개발완료] {item_id} {display}",
        body="\n".join([
            f"BIM Command Center Add-in 스캐폴드: {display}",
            f"ID: {item_id}  타입: {kind}",
            f"완료: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "", "파일:",
            *[f"  {f.name} ({f.stat().st_size:,} bytes)" for f in files],
        ]),
        attachments=files,
    )
    print(f"  이메일: {result}")


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# ═════════════════════════════════════════════════════════════════
# ① 누락 UI — R-04 ElementRenumbering XAML
# ═════════════════════════════════════════════════════════════════
async def missing_r04_ui() -> list[Path]:
    out = REVIT_ROOT / "ElementRenumbering"
    files = []

    files.append(write(out / "ElementRenumberingWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.ElementRenumberingWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Element Renumbering" Height="280" Width="360"
        ResizeMode="NoResize" WindowStartupLocation="CenterScreen">
    <Grid Margin="12">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <StackPanel Grid.Row="0" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="카테고리:" Width="80" VerticalAlignment="Center"/>
            <ComboBox x:Name="CboCategory" Width="220">
                <ComboBoxItem Content="Rooms" IsSelected="True"/>
                <ComboBoxItem Content="Doors"/>
                <ComboBoxItem Content="Spaces"/>
            </ComboBox>
        </StackPanel>
        <StackPanel Grid.Row="1" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="파라미터:" Width="80" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtParam" Width="220" Text="Number"/>
        </StackPanel>
        <StackPanel Grid.Row="2" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="접두사:" Width="80" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtPrefix" Width="100"/>
            <TextBlock Text="시작번호:" Width="60" VerticalAlignment="Center" Margin="8,0,0,0"/>
            <TextBox x:Name="TxtStart" Width="50" Text="1"/>
        </StackPanel>
        <StackPanel Grid.Row="3" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="증분:" Width="80" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtStep" Width="50" Text="1"/>
            <TextBlock Text="자릿수:" Width="60" VerticalAlignment="Center" Margin="8,0,0,0"/>
            <TextBox x:Name="TxtDigits" Width="50" Text="0"/>
        </StackPanel>
        <StackPanel Grid.Row="4" Orientation="Horizontal" Margin="0,0,0,12">
            <TextBlock Text="정렬기준:" Width="80" VerticalAlignment="Center"/>
            <ComboBox x:Name="CboSort" Width="160">
                <ComboBoxItem Content="선택 순서" IsSelected="True"/>
                <ComboBoxItem Content="X 좌표"/>
                <ComboBoxItem Content="Y 좌표"/>
                <ComboBoxItem Content="레벨"/>
            </ComboBox>
        </StackPanel>
        <StackPanel Grid.Row="7" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="미리보기 후 실행" Width="110" Margin="4,0" Click="BtnOk_Click"/>
            <Button Content="취소" Width="60" Click="BtnCancel_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))

    files.append(write(out / "RenumberPreviewWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Windows;

namespace BIMCommandCenter.Commands
{
    public partial class RenumberPreviewWindow : Window
    {
        public RenumberPreviewWindow(List<RenumberPreview> previews)
        {
            InitializeComponent();
            Grid.ItemsSource = previews;
        }
        private void BtnOk_Click(object s, RoutedEventArgs e)     => DialogResult = true;
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }
}
"""))

    files.append(write(out / "RenumberPreviewWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.RenumberPreviewWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="번호 재배정 미리보기" Height="400" Width="500"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="8">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <DataGrid x:Name="Grid" Grid.Row="0" AutoGenerateColumns="False"
                  IsReadOnly="True" Margin="0,0,0,8">
            <DataGrid.Columns>
                <DataGridTextColumn Header="현재 번호" Binding="{Binding OldNumber}" Width="150"/>
                <DataGridTextColumn Header="변경 번호"  Binding="{Binding NewNumber}" Width="150"/>
            </DataGrid.Columns>
        </DataGrid>
        <StackPanel Grid.Row="1" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="적용" Width="80" Margin="4,0" Click="BtnOk_Click"/>
            <Button Content="취소" Width="80" Click="BtnCancel_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    return files


# ② 누락 UI — R-05 ProjectCleanupLite WPF Window
async def missing_r05_ui() -> list[Path]:
    out = REVIT_ROOT / "ProjectCleanupLite"
    files = []

    files.append(write(out / "ProjectCleanupWindow.xaml.cs", """\
using System.IO;
using System.Windows;
using Newtonsoft.Json;

namespace BIMCommandCenter.Commands
{
    public partial class ProjectCleanupWindow : Window
    {
        private readonly CleanupAuditReport _report;
        public ProjectCleanupWindow(CleanupAuditReport report)
        {
            _report = report;
            InitializeComponent();
            TxtSummary.Text =
                $"미배치 뷰: {report.UnplacedViews}개\\n" +
                $"CAD Import: {report.CadImports}개\\n" +
                $"경고 합계: {report.TotalWarnings}개\\n" +
                $"미배치 룸: {report.UnplacedRooms}개\\n" +
                $"미사용 뷰 템플릿: {report.UnusedViewTemplates}개";
            LstWarnings.ItemsSource = report.WarningByType;
            LstViews.ItemsSource    = report.UnplacedViewNames;
        }
        private void BtnExport_Click(object s, RoutedEventArgs e)
        {
            var dlg = new Microsoft.Win32.SaveFileDialog
                { Filter = "JSON|*.json", FileName = "ProjectCleanupReport.json" };
            if (dlg.ShowDialog() != true) return;
            File.WriteAllText(dlg.FileName,
                JsonConvert.SerializeObject(_report, Formatting.Indented));
            MessageBox.Show($"저장: {dlg.FileName}");
        }
        private void BtnClose_Click(object s, RoutedEventArgs e) => Close();
    }
}
"""))

    files.append(write(out / "ProjectCleanupWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.ProjectCleanupWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Project Cleanup Lite — 감사 결과" Height="520" Width="560"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="12">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <TextBlock Grid.Row="0" Text="요약" FontWeight="Bold" Margin="0,0,0,4"/>
        <TextBox  Grid.Row="1" x:Name="TxtSummary" IsReadOnly="True"
                  TextWrapping="Wrap" Margin="0,0,0,8" Background="#F5F5F5" Padding="4"/>
        <TextBlock Grid.Row="2" Text="경고 유형별 집계" FontWeight="Bold" Margin="0,0,0,4"/>
        <ListBox  Grid.Row="3" x:Name="LstWarnings" Height="140" Margin="0,0,0,8"/>
        <TextBlock Grid.Row="4" Text="미배치 뷰 목록 (최대 50개)" FontWeight="Bold" Margin="0,0,0,4"/>
        <ListBox  Grid.Row="5" x:Name="LstViews" Height="100" Margin="0,0,0,8"/>
        <StackPanel Grid.Row="5" Orientation="Horizontal" HorizontalAlignment="Right"
                    VerticalAlignment="Bottom">
            <Button Content="JSON 저장" Width="90" Margin="4,0" Click="BtnExport_Click"/>
            <Button Content="닫기"      Width="70" Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    return files


# ③ 누락 UI — N-01 ClashBoardForm (WinForms)
async def missing_n01_ui() -> list[Path]:
    out = NAV_ROOT / "ClashResponsibilityBoard" / "src"
    files = []
    files.append(write(out / "ClashBoardForm.cs", """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;

namespace NavisworksClashBoard
{
    public class ClashBoardForm : Form
    {
        private readonly List<ClashItem> _items;
        private readonly string _rulesPath;
        private DataGridView _grid;
        private Button _btnExcel, _btnClose;

        public ClashBoardForm(List<ClashItem> items, string rulesPath)
        {
            _items     = items;
            _rulesPath = rulesPath;
            Text       = $"간섭 책임자 배정 보드 ({items.Count}건)";
            Width      = 900; Height = 560;
            StartPosition = FormStartPosition.CenterScreen;
            BuildUI();
        }

        private void BuildUI()
        {
            _grid = new DataGridView
            {
                Dock = DockStyle.Fill, ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells,
                DataSource = _items,
            };
            var panel = new FlowLayoutPanel { Dock = DockStyle.Bottom, Height = 40 };
            _btnExcel = new Button { Text = "엑셀 저장", Width = 100 };
            _btnClose = new Button { Text = "닫기",      Width = 80  };
            _btnExcel.Click += BtnExcel_Click;
            _btnClose.Click += (s, e) => Close();
            panel.Controls.AddRange(new Control[] { _btnExcel, _btnClose });
            Controls.Add(_grid);
            Controls.Add(panel);
        }

        private void BtnExcel_Click(object s, EventArgs e)
        {
            var dlg = new SaveFileDialog
                { Filter = "Excel|*.xlsx", FileName = "ClashResponsibility.xlsx" };
            if (dlg.ShowDialog() != DialogResult.OK) return;
            ReportGenerator.GenerateExcel(_items, dlg.FileName);
            MessageBox.Show($"저장 완료: {dlg.FileName}");
        }
    }
}
"""))
    return files


# ④ 누락 UI — N-02 ClashGroupForm
async def missing_n02_ui() -> list[Path]:
    out = NAV_ROOT / "ClashGroupEngine" / "src"
    files = []
    files.append(write(out / "ClashGroupForm.cs", """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;

namespace NavisworksClashGroup
{
    public class ClashGroupForm : Form
    {
        private readonly Document _doc;
        private readonly string _rulesPath;
        private ListBox  _lstTests, _lstGroups;
        private DataGridView _grid;
        private List<ClashGroupRule> _rules = new();
        private static readonly string DefaultRulesPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
            "BCC_ClashGroupRules.json");

        public ClashGroupForm(Document doc)
        {
            _doc = doc;
            _rulesPath = DefaultRulesPath;
            if (!File.Exists(_rulesPath)) ClashGroupEngine.SaveRules(_rulesPath,
                new List<ClashGroupRule>
                {
                    new() { GroupName="활성 클래시",  Keywords=new(){""},    Statuses=new(){"Active"}   },
                    new() { GroupName="승인 클래시",  Keywords=new(){""},    Statuses=new(){"Approved"} },
                    new() { GroupName="해결된 클래시", Keywords=new(){""},   Statuses=new(){"Resolved"} },
                });
            _rules = ClashGroupEngine.LoadRules(_rulesPath);
            Text   = "클래시 그룹화";
            Width  = 760; Height = 480;
            StartPosition = FormStartPosition.CenterScreen;
            BuildUI();
        }

        private void BuildUI()
        {
            var split = new SplitContainer { Dock = DockStyle.Fill, SplitterDistance = 200 };

            // 좌측: 테스트 목록
            _lstTests = new ListBox { Dock = DockStyle.Fill };
            var clashPlugin = ClashPlugin.GetClashPlugin();
            if (clashPlugin != null)
                foreach (ClashTest t in clashPlugin.TestsData.Tests)
                    _lstTests.Items.Add(t.DisplayName);
            split.Panel1.Controls.Add(_lstTests);

            // 우측: 결과 그리드
            _grid = new DataGridView
            {
                Dock = DockStyle.Fill, ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells,
            };
            _grid.Columns.AddRange(
                new DataGridViewTextBoxColumn { HeaderText = "그룹",    Name = "Group"  },
                new DataGridViewTextBoxColumn { HeaderText = "클래시 수", Name = "Count" });
            split.Panel2.Controls.Add(_grid);

            var btnRun   = new Button { Text = "그룹화 실행", Dock = DockStyle.Bottom, Height = 32 };
            var btnClose = new Button { Text = "닫기",       Dock = DockStyle.Bottom, Height = 32 };
            btnRun.Click   += BtnRun_Click;
            btnClose.Click += (s, e) => Close();

            Controls.Add(split);
            Controls.Add(btnRun);
            Controls.Add(btnClose);
        }

        private void BtnRun_Click(object s, EventArgs e)
        {
            if (_lstTests.SelectedIndex < 0) { MessageBox.Show("테스트를 선택하세요."); return; }
            var plugin = ClashPlugin.GetClashPlugin();
            if (plugin == null) return;
            var test   = plugin.TestsData.Tests.ElementAt(_lstTests.SelectedIndex);
            var groups = ClashGroupEngine.GroupClashes(test, _rules);
            _grid.Rows.Clear();
            foreach (var kv in groups)
                _grid.Rows.Add(kv.Key, kv.Value.Count);
        }
    }
}
"""))
    return files


# ⑤ 누락 UI — N-03 ClashTestDefinerForm
async def missing_n03_ui() -> list[Path]:
    out = NAV_ROOT / "ClashTestDefiner" / "src"
    files = []
    files.append(write(out / "ClashTestDefinerForm.cs", """\
using System;
using System.Windows.Forms;
using Autodesk.Navisworks.Api;

namespace NavisworksClashDefiner
{
    public class ClashTestDefinerForm : Form
    {
        private readonly Document _doc;
        private TextBox _txtPath, _txtResult;
        private ComboBox _cboPolicy;
        private Button _btnBrowse, _btnDry, _btnRun, _btnClose;

        public ClashTestDefinerForm(Document doc)
        {
            _doc  = doc;
            Text  = "간섭 테스트 일괄 정의";
            Width = 520; Height = 420;
            StartPosition = FormStartPosition.CenterScreen;
            BuildUI();
        }

        private void BuildUI()
        {
            var lbl1   = new Label { Text = "JSON 파일:", Top = 16, Left = 10, Width = 80 };
            _txtPath   = new TextBox { Top = 14, Left = 95, Width = 300, ReadOnly = true };
            _btnBrowse = new Button  { Text = "...", Top = 12, Left = 400, Width = 40 };
            var lbl2   = new Label { Text = "중복 처리:", Top = 50, Left = 10, Width = 80 };
            _cboPolicy = new ComboBox { Top = 48, Left = 95, Width = 120, DropDownStyle = ComboBoxStyle.DropDownList };
            _cboPolicy.Items.AddRange(new[] { "스킵(기본)", "대체" });
            _cboPolicy.SelectedIndex = 0;
            _txtResult = new TextBox
            {
                Top = 90, Left = 10, Width = 480, Height = 220,
                Multiline = true, ScrollBars = ScrollBars.Vertical, ReadOnly = true,
            };
            _btnDry   = new Button { Text = "Dry-Run",  Top = 325, Left = 10,  Width = 100 };
            _btnRun   = new Button { Text = "실행",      Top = 325, Left = 120, Width = 80  };
            _btnClose = new Button { Text = "닫기",      Top = 325, Left = 210, Width = 80  };

            _btnBrowse.Click += (s, e) =>
            {
                var dlg = new OpenFileDialog { Filter = "JSON|*.json" };
                if (dlg.ShowDialog() == DialogResult.OK) _txtPath.Text = dlg.FileName;
            };
            _btnDry.Click += (s, e) => RunWith(dryRun: true);
            _btnRun.Click += (s, e) => RunWith(dryRun: false);
            _btnClose.Click += (s, e) => Close();

            Controls.AddRange(new Control[]
                { lbl1, _txtPath, _btnBrowse, lbl2, _cboPolicy, _txtResult,
                  _btnDry, _btnRun, _btnClose });
        }

        private void RunWith(bool dryRun)
        {
            if (string.IsNullOrEmpty(_txtPath.Text))
            { MessageBox.Show("JSON 파일을 선택하세요."); return; }
            var defs   = ClashTestDefinerEngine.LoadJson(_txtPath.Text);
            var policy = _cboPolicy.SelectedIndex == 0 ? DuplicatePolicy.Skip : DuplicatePolicy.Replace;
            var result = dryRun
                ? ClashTestDefinerEngine.DryRun(_doc, defs, policy)
                : ClashTestDefinerEngine.Execute(_doc, defs, policy);
            _txtResult.Text =
                $"생성: {result.Created}  스킵: {result.Skipped}\r\n\r\n" +
                string.Join("\r\n", result.Log);
        }
    }
}
"""))
    return files


# ═════════════════════════════════════════════════════════════════
# Phase 2 Revit 아이템
# ═════════════════════════════════════════════════════════════════

# R-06  Line Cleanup Lite
async def build_r06() -> list[Path]:
    out = REVIT_ROOT / "LineCleanupLite"
    out.mkdir(parents=True, exist_ok=True)
    files = []

    engine = """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public class LineCleanupReport
    {
        public int DuplicateLines { get; set; }
        public int ShortLines     { get; set; }
        public int ModelLines     { get; set; }
        public List<ElementId> DuplicateIds { get; } = new();
        public List<ElementId> ShortIds     { get; } = new();
        public List<ElementId> ModelLineIds { get; } = new();
    }

    public static class LineCleanupEngine
    {
        public static LineCleanupReport Audit(View view, Document doc, double shortThresholdMm = 10)
        {
            var report = new LineCleanupReport();
            double threshold = shortThresholdMm / 304.8; // mm → feet

            var detailLines = new FilteredElementCollector(doc, view.Id)
                .OfClass(typeof(CurveElement)).Cast<CurveElement>().ToList();

            // 짧은 선
            foreach (var line in detailLines)
            {
                if (line.GeometryCurve?.Length < threshold)
                {
                    report.ShortLines++;
                    report.ShortIds.Add(line.Id);
                }
            }

            // 중복 선 (같은 시작/끝점 ± 1mm)
            double tol = 1.0 / 304.8;
            for (int i = 0; i < detailLines.Count; i++)
            for (int j = i + 1; j < detailLines.Count; j++)
            {
                // QWEN_FILL: detailLines[i] 와 detailLines[j] 의 GeometryCurve 시작/끝점 비교
                // 차이가 tol 이내이면 둘 다 DuplicateIds 에 추가 (중복 방지)
                var ci = detailLines[i].GeometryCurve;
                var cj = detailLines[j].GeometryCurve;
                if (ci == null || cj == null) continue;
                bool dup = (ci.GetEndPoint(0).DistanceTo(cj.GetEndPoint(0)) < tol &&
                            ci.GetEndPoint(1).DistanceTo(cj.GetEndPoint(1)) < tol) ||
                           (ci.GetEndPoint(0).DistanceTo(cj.GetEndPoint(1)) < tol &&
                            ci.GetEndPoint(1).DistanceTo(cj.GetEndPoint(0)) < tol);
                if (dup && !report.DuplicateIds.Contains(detailLines[j].Id))
                    report.DuplicateIds.Add(detailLines[j].Id);
            }
            report.DuplicateLines = report.DuplicateIds.Count;

            // 모델 선 목록 (ModelLine in view)
            var modelLines = new FilteredElementCollector(doc, view.Id)
                .OfClass(typeof(ModelCurve)).Cast<ModelCurve>()
                .Where(mc => mc is ModelLine).ToList();
            report.ModelLines = modelLines.Count;
            report.ModelLineIds.AddRange(modelLines.Select(m => m.Id));

            return report;
        }

        public static int DeleteLines(Document doc, IEnumerable<ElementId> ids)
        {
            int cnt = 0;
            foreach (var id in ids)
            { doc.Delete(id); cnt++; }
            return cnt;
        }
    }
}
"""
    files.append(write(out / "LineCleanupEngine.cs",
        await qwen_fill(engine, "Revit CurveElement.GeometryCurve, GetEndPoint, DistanceTo")))

    files.append(write(out / "LineCleanupCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class LineCleanupCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var uiDoc = data.Application.ActiveUIDocument;
            var doc   = uiDoc.Document;
            var view  = uiDoc.ActiveView;

            var report = LineCleanupEngine.Audit(view, doc);
            var win    = new LineCleanupWindow(report);
            if (win.ShowDialog() != true) return Result.Cancelled;

            var toDelete = new System.Collections.Generic.List<ElementId>();
            if (win.DeleteDuplicates) toDelete.AddRange(report.DuplicateIds);
            if (win.DeleteShort)      toDelete.AddRange(report.ShortIds);
            if (toDelete.Count == 0)  return Result.Succeeded;

            using (var tx = new Transaction(doc, "BCC - Line Cleanup"))
            {
                tx.Start();
                int cnt = LineCleanupEngine.DeleteLines(doc, toDelete);
                tx.Commit();
                TaskDialog.Show("완료", $"{cnt}개 선 삭제 완료.");
            }
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "LineCleanupWindow.xaml.cs", """\
using System.Windows;

namespace BIMCommandCenter.Commands
{
    public partial class LineCleanupWindow : Window
    {
        public bool DeleteDuplicates { get; private set; }
        public bool DeleteShort      { get; private set; }

        public LineCleanupWindow(LineCleanupReport report)
        {
            InitializeComponent();
            TxtSummary.Text =
                $"중복 선: {report.DuplicateLines}개  |  " +
                $"짧은 선: {report.ShortLines}개  |  " +
                $"모델 선(참고): {report.ModelLines}개";
        }
        private void BtnOk_Click(object s, RoutedEventArgs e)
        {
            DeleteDuplicates = ChkDuplicate.IsChecked == true;
            DeleteShort      = ChkShort.IsChecked == true;
            DialogResult = true;
        }
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }
}
"""))

    files.append(write(out / "LineCleanupWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.LineCleanupWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Line Cleanup Lite" Height="200" Width="380"
        ResizeMode="NoResize" WindowStartupLocation="CenterScreen">
    <StackPanel Margin="16">
        <TextBlock x:Name="TxtSummary" TextWrapping="Wrap" Margin="0,0,0,12"/>
        <CheckBox x:Name="ChkDuplicate" Content="중복 선 삭제" IsChecked="True" Margin="0,0,0,6"/>
        <CheckBox x:Name="ChkShort"     Content="짧은 선 삭제 (10mm 이하)" Margin="0,0,0,12"/>
        <StackPanel Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="실행" Width="80" Margin="4,0" Click="BtnOk_Click"/>
            <Button Content="취소" Width="80" Click="BtnCancel_Click"/>
        </StackPanel>
    </StackPanel>
</Window>
"""))
    print(f"  [R-06] LineCleanupLite — {len(files)}개")
    return files


# R-07  Smart Selector Lite
async def build_r07() -> list[Path]:
    out = REVIT_ROOT / "SmartSelectorLite"
    out.mkdir(parents=True, exist_ok=True)
    files = []

    engine = """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Newtonsoft.Json;

namespace BIMCommandCenter.Commands
{
    public enum SelectorScope { ActiveView, WholeProject }
    public enum FilterOperator { Equals, Contains, StartsWith, EndsWith, Exists, Missing }

    public class SelectorFilter
    {
        [JsonProperty("category")]   public string Category   { get; set; }
        [JsonProperty("familyName")] public string FamilyName { get; set; }
        [JsonProperty("typeName")]   public string TypeName   { get; set; }
        [JsonProperty("workset")]    public string Workset    { get; set; }
        [JsonProperty("paramName")]  public string ParamName  { get; set; }
        [JsonProperty("op")]         public FilterOperator Op { get; set; } = FilterOperator.Exists;
        [JsonProperty("value")]      public string Value      { get; set; }
    }

    public static class SmartSelectorEngine
    {
        public static List<ElementId> Run(Document doc, View view,
            SelectorScope scope, SelectorFilter filter)
        {
            // QWEN_FILL: scope 에 따라 collector 범위 결정, filter 조건 적용
            FilteredElementCollector collector = scope == SelectorScope.ActiveView
                ? new FilteredElementCollector(doc, view.Id)
                : new FilteredElementCollector(doc);

            collector.WhereElementIsNotElementType();

            IEnumerable<Element> elems = collector;

            if (!string.IsNullOrEmpty(filter.Category))
            {
                var bic = TryGetBic(filter.Category);
                if (bic.HasValue)
                    elems = collector.OfCategory(bic.Value).Cast<Element>();
            }

            if (!string.IsNullOrEmpty(filter.FamilyName))
                elems = elems.Where(e => (e as FamilyInstance)?.Symbol?.FamilyName == filter.FamilyName);

            if (!string.IsNullOrEmpty(filter.TypeName))
                elems = elems.Where(e => (e as FamilyInstance)?.Symbol?.Name == filter.TypeName);

            if (!string.IsNullOrEmpty(filter.ParamName))
                elems = elems.Where(e => MatchParam(e, filter));

            return elems.Select(e => e.Id).ToList();
        }

        private static bool MatchParam(Element e, SelectorFilter f)
        {
            var p = e.LookupParameter(f.ParamName);
            string val = p?.AsValueString() ?? p?.AsString() ?? "";
            return f.Op switch
            {
                FilterOperator.Exists     => p != null,
                FilterOperator.Missing    => p == null,
                FilterOperator.Equals     => val.Equals(f.Value, StringComparison.OrdinalIgnoreCase),
                FilterOperator.Contains   => val.Contains(f.Value),
                FilterOperator.StartsWith => val.StartsWith(f.Value),
                FilterOperator.EndsWith   => val.EndsWith(f.Value),
                _                         => false,
            };
        }

        private static BuiltInCategory? TryGetBic(string name)
        {
            if (Enum.TryParse<BuiltInCategory>("OST_" + name, out var bic)) return bic;
            return null;
        }
    }
}
"""
    files.append(write(out / "SmartSelectorEngine.cs",
        await qwen_fill(engine, "Revit FilteredElementCollector, FamilyInstance.Symbol.FamilyName, LookupParameter")))

    files.append(write(out / "SmartSelectorCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.ReadOnly)]
    [Regeneration(RegenerationOption.Manual)]
    public class SmartSelectorCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var uiDoc = data.Application.ActiveUIDocument;
            var win   = new SmartSelectorWindow(uiDoc.Document, uiDoc.ActiveView);
            win.ShowDialog();
            if (win.SelectedIds?.Count > 0)
                uiDoc.Selection.SetElementIds(win.SelectedIds);
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "SmartSelectorWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Windows;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public partial class SmartSelectorWindow : Window
    {
        private readonly Document _doc;
        private readonly View     _view;
        public IList<ElementId> SelectedIds { get; private set; }

        public SmartSelectorWindow(Document doc, View view)
        {
            _doc = doc; _view = view;
            InitializeComponent();
        }

        private void BtnPreview_Click(object s, RoutedEventArgs e)
        {
            var filter = BuildFilter();
            var scope  = (CboScope.SelectedIndex == 0)
                ? SelectorScope.ActiveView : SelectorScope.WholeProject;
            var ids = SmartSelectorEngine.Run(_doc, _view, scope, filter);
            TxtCount.Text = $"매칭 요소: {ids.Count}개";
            SelectedIds = ids;
        }
        private void BtnApply_Click(object s, RoutedEventArgs e)  { DialogResult = true; }
        private void BtnClose_Click(object s, RoutedEventArgs e)  => Close();

        private SelectorFilter BuildFilter() => new SelectorFilter
        {
            Category  = TxtCategory.Text.Trim(),
            FamilyName = TxtFamily.Text.Trim(),
            TypeName  = TxtType.Text.Trim(),
            ParamName = TxtParam.Text.Trim(),
            Value     = TxtValue.Text.Trim(),
            Op        = (FilterOperator)CboOp.SelectedIndex,
        };
    }
}
"""))

    files.append(write(out / "SmartSelectorWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.SmartSelectorWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Smart Selector Lite" Height="340" Width="400"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="12">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <StackPanel Grid.Row="0" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="범위:" Width="80" VerticalAlignment="Center"/>
            <ComboBox x:Name="CboScope" Width="200">
                <ComboBoxItem Content="현재 뷰" IsSelected="True"/>
                <ComboBoxItem Content="전체 프로젝트"/>
            </ComboBox>
        </StackPanel>
        <StackPanel Grid.Row="1" Orientation="Horizontal" Margin="0,0,0,4">
            <TextBlock Text="카테고리:" Width="80" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtCategory" Width="200" ToolTip="예: Walls, Pipes"/>
        </StackPanel>
        <StackPanel Grid.Row="2" Orientation="Horizontal" Margin="0,0,0,4">
            <TextBlock Text="패밀리명:" Width="80" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtFamily"   Width="200"/>
        </StackPanel>
        <StackPanel Grid.Row="3" Orientation="Horizontal" Margin="0,0,0,4">
            <TextBlock Text="타입명:"    Width="80" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtType"    Width="200"/>
        </StackPanel>
        <StackPanel Grid.Row="4" Orientation="Horizontal" Margin="0,0,0,4">
            <TextBlock Text="파라미터:"  Width="80" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtParam"   Width="140"/>
            <ComboBox x:Name="CboOp" Width="56" Margin="4,0,0,0" SelectedIndex="0">
                <ComboBoxItem Content="="/>
                <ComboBoxItem Content="포함"/>
                <ComboBoxItem Content="시작"/>
                <ComboBoxItem Content="끝"/>
                <ComboBoxItem Content="있음"/>
                <ComboBoxItem Content="없음"/>
            </ComboBox>
        </StackPanel>
        <StackPanel Grid.Row="5" Orientation="Horizontal" Margin="0,0,0,12">
            <TextBlock Text="값:"        Width="80" VerticalAlignment="Center"/>
            <TextBox x:Name="TxtValue"   Width="200"/>
        </StackPanel>
        <TextBlock Grid.Row="6" x:Name="TxtCount" Margin="0,0,0,8" Foreground="DarkBlue"/>
        <StackPanel Grid.Row="7" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="미리보기" Width="80" Margin="4,0" Click="BtnPreview_Click"/>
            <Button Content="선택 적용" Width="80" Margin="4,0" Click="BtnApply_Click"/>
            <Button Content="닫기"      Width="60" Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [R-07] SmartSelectorLite — {len(files)}개")
    return files


# R-08  Workset Inspector Lite
async def build_r08() -> list[Path]:
    out = REVIT_ROOT / "WorksetInspectorLite"
    out.mkdir(parents=True, exist_ok=True)
    files = []

    engine = """\
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public class WorksetSummary
    {
        public string WorksetName  { get; set; }
        public int    ElementCount { get; set; }
        public List<string> FlaggedCategories { get; } = new();
    }

    public static class WorksetInspectorEngine
    {
        public static List<WorksetSummary> Inspect(Document doc)
        {
            // QWEN_FILL: FilteredWorksetCollector 로 UserWorkset 목록 수집,
            // 각 워크셋의 요소 수를 FilteredElementCollector + WorksetFilter 로 집계
            var result = new List<WorksetSummary>();
            var worksets = new FilteredWorksetCollector(doc)
                .OfKind(WorksetKind.UserWorkset).ToList();

            foreach (var ws in worksets)
            {
                var filter = new ElementWorksetFilter(ws.Id);
                int cnt = new FilteredElementCollector(doc)
                    .WherePasses(filter)
                    .WhereElementIsNotElementType()
                    .Count();
                result.Add(new WorksetSummary { WorksetName = ws.Name, ElementCount = cnt });
            }
            return result.OrderByDescending(w => w.ElementCount).ToList();
        }

        public static List<ElementId> GetElementsInWorkset(Document doc, string worksetName)
        {
            var ws = new FilteredWorksetCollector(doc)
                .OfKind(WorksetKind.UserWorkset)
                .FirstOrDefault(w => w.Name == worksetName);
            if (ws == null) return new List<ElementId>();
            return new FilteredElementCollector(doc)
                .WherePasses(new ElementWorksetFilter(ws.Id))
                .WhereElementIsNotElementType()
                .Select(e => e.Id).ToList();
        }
    }
}
"""
    files.append(write(out / "WorksetInspectorEngine.cs",
        await qwen_fill(engine, "Revit FilteredWorksetCollector.OfKind(WorksetKind.UserWorkset), ElementWorksetFilter")))

    files.append(write(out / "WorksetInspectorCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.ReadOnly)]
    [Regeneration(RegenerationOption.Manual)]
    public class WorksetInspectorCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var uiDoc    = data.Application.ActiveUIDocument;
            var doc      = uiDoc.Document;
            var summaries = WorksetInspectorEngine.Inspect(doc);
            var win = new WorksetInspectorWindow(summaries, doc, uiDoc);
            win.ShowDialog();
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "WorksetInspectorWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    public partial class WorksetInspectorWindow : Window
    {
        private readonly Document   _doc;
        private readonly UIDocument _uiDoc;

        public WorksetInspectorWindow(List<WorksetSummary> summaries,
            Document doc, UIDocument uiDoc)
        {
            _doc = doc; _uiDoc = uiDoc;
            InitializeComponent();
            DgWorksets.ItemsSource = summaries;
        }

        private void BtnSelect_Click(object s, RoutedEventArgs e)
        {
            if (DgWorksets.SelectedItem is not WorksetSummary ws) return;
            var ids = WorksetInspectorEngine.GetElementsInWorkset(_doc, ws.WorksetName);
            _uiDoc.Selection.SetElementIds(ids);
            TxtStatus.Text = $"'{ws.WorksetName}' 요소 {ids.Count}개 선택됨";
        }
        private void BtnClose_Click(object s, RoutedEventArgs e) => Close();
    }
}
"""))

    files.append(write(out / "WorksetInspectorWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.WorksetInspectorWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Workset Inspector Lite" Height="420" Width="480"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="8">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <DataGrid x:Name="DgWorksets" Grid.Row="0" AutoGenerateColumns="False"
                  IsReadOnly="True" SelectionMode="Single" Margin="0,0,0,8">
            <DataGrid.Columns>
                <DataGridTextColumn Header="워크셋"   Binding="{Binding WorksetName}"  Width="*"/>
                <DataGridTextColumn Header="요소 수"  Binding="{Binding ElementCount}" Width="80"/>
            </DataGrid.Columns>
        </DataGrid>
        <TextBlock Grid.Row="1" x:Name="TxtStatus" Margin="0,0,0,8" Foreground="DarkBlue"/>
        <StackPanel Grid.Row="2" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="선택 적용" Width="90" Margin="4,0" Click="BtnSelect_Click"/>
            <Button Content="닫기"      Width="70" Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [R-08] WorksetInspectorLite — {len(files)}개")
    return files


# R-09  Link Health & Reload
async def build_r09() -> list[Path]:
    out = REVIT_ROOT / "LinkHealthReload"
    out.mkdir(parents=True, exist_ok=True)
    files = []

    engine = """\
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public enum LinkStatus { Loaded, Unloaded, NotFound }

    public class LinkInfo
    {
        public string     Name   { get; set; }
        public string     Path   { get; set; }
        public LinkStatus Status { get; set; }
        public string     Type   { get; set; }   // "Revit" | "CAD"
        public ElementId  Id     { get; set; }
    }

    public static class LinkHealthEngine
    {
        public static List<LinkInfo> Audit(Document doc)
        {
            var list = new List<LinkInfo>();

            // Revit Links
            foreach (var instance in new FilteredElementCollector(doc)
                .OfClass(typeof(RevitLinkInstance)).Cast<RevitLinkInstance>())
            {
                var type = doc.GetElement(instance.GetTypeId()) as RevitLinkType;
                list.Add(new LinkInfo
                {
                    Id     = instance.Id,
                    Name   = type?.Name ?? "Unknown",
                    Path   = type?.GetExternalFileReference()?.GetAbsolutePath() ?? "",
                    Status = type?.GetLinkedFileStatus() == LinkedFileStatus.Loaded
                             ? LinkStatus.Loaded
                             : type?.GetLinkedFileStatus() == LinkedFileStatus.Unloaded
                               ? LinkStatus.Unloaded : LinkStatus.NotFound,
                    Type   = "Revit",
                });
            }

            // CAD Links
            // QWEN_FILL: ImportInstance (IsLinked==true) 로 CAD 링크 수집
            foreach (var imp in new FilteredElementCollector(doc)
                .OfClass(typeof(ImportInstance)).Cast<ImportInstance>()
                .Where(i => i.IsLinked))
            {
                list.Add(new LinkInfo
                {
                    Id   = imp.Id, Name = imp.Category?.Name ?? "CAD",
                    Path = "", Status = LinkStatus.Loaded, Type = "CAD",
                });
            }
            return list;
        }

        public static int ReloadLinks(Document doc, IEnumerable<ElementId> ids)
        {
            int cnt = 0;
            foreach (var id in ids)
            {
                if (doc.GetElement(id) is RevitLinkInstance inst)
                {
                    var type = doc.GetElement(inst.GetTypeId()) as RevitLinkType;
                    type?.Reload();
                    cnt++;
                }
            }
            return cnt;
        }
    }
}
"""
    files.append(write(out / "LinkHealthEngine.cs",
        await qwen_fill(engine, "Revit RevitLinkInstance, RevitLinkType.GetLinkedFileStatus(), Reload()")))

    files.append(write(out / "LinkHealthCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class LinkHealthCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc   = data.Application.ActiveUIDocument.Document;
            var links = LinkHealthEngine.Audit(doc);
            var win   = new LinkHealthWindow(links);
            if (win.ShowDialog() != true) return Result.Cancelled;

            if (win.ReloadIds.Count > 0)
            {
                using var tx = new Transaction(doc, "BCC - Reload Links");
                tx.Start();
                int cnt = LinkHealthEngine.ReloadLinks(doc, win.ReloadIds);
                tx.Commit();
                TaskDialog.Show("완료", $"{cnt}개 링크 리로드 완료.");
            }
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "LinkHealthWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public partial class LinkHealthWindow : Window
    {
        public List<ElementId> ReloadIds { get; } = new();
        public LinkHealthWindow(List<LinkInfo> links)
        {
            InitializeComponent();
            DgLinks.ItemsSource = links;
        }
        private void BtnReload_Click(object s, RoutedEventArgs e)
        {
            ReloadIds.Clear();
            ReloadIds.AddRange(DgLinks.SelectedItems.Cast<LinkInfo>().Select(l => l.Id));
            DialogResult = true;
        }
        private void BtnClose_Click(object s, RoutedEventArgs e) => Close();
    }
}
"""))

    files.append(write(out / "LinkHealthWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.LinkHealthWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Link Health &amp; Reload" Height="380" Width="580"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="8">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <DataGrid x:Name="DgLinks" Grid.Row="0" AutoGenerateColumns="False"
                  SelectionMode="Extended" Margin="0,0,0,8">
            <DataGrid.Columns>
                <DataGridTextColumn Header="이름"   Binding="{Binding Name}"   Width="*"/>
                <DataGridTextColumn Header="타입"   Binding="{Binding Type}"   Width="60"/>
                <DataGridTextColumn Header="상태"   Binding="{Binding Status}" Width="90"/>
            </DataGrid.Columns>
        </DataGrid>
        <StackPanel Grid.Row="1" Orientation="Horizontal" HorizontalAlignment="Right">
            <TextBlock Text="선택 항목 리로드 가능" VerticalAlignment="Center" Margin="0,0,12,0" Foreground="Gray"/>
            <Button Content="선택 리로드" Width="100" Margin="4,0" Click="BtnReload_Click"/>
            <Button Content="닫기"        Width="70" Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [R-09] LinkHealthReload — {len(files)}개")
    return files


# R-10  Schedule Excel Export (Revit 측)
async def build_r10() -> list[Path]:
    out = REVIT_ROOT / "ScheduleExcelExport"
    out.mkdir(parents=True, exist_ok=True)
    files = []

    engine = """\
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Revit.DB;
using ClosedXML.Excel;

namespace BIMCommandCenter.Commands
{
    public class ScheduleExportResult
    {
        public int RowCount    { get; set; }
        public int ColumnCount { get; set; }
        public string FilePath { get; set; }
    }

    public static class ScheduleExportEngine
    {
        public static ScheduleExportResult Export(ViewSchedule schedule, string outputPath)
        {
            // QWEN_FILL: schedule.GetTableData(), ViewScheduleTable.GetSectionData() 로
            // 헤더(GetCellText row=0)와 데이터 행을 읽어 ClosedXML 엑셀로 저장
            var tableData   = schedule.GetTableData();
            var sectionData = tableData.GetSectionData(SectionType.Body);
            int rowCount    = sectionData.NumberOfRows;
            int colCount    = sectionData.NumberOfColumns;

            using var wb = new XLWorkbook();
            var ws = wb.Worksheets.Add(schedule.Name.Length > 31
                ? schedule.Name.Substring(0, 31) : schedule.Name);

            for (int r = 0; r < rowCount; r++)
            for (int c = 0; c < colCount; c++)
            {
                string text = sectionData.GetCellText(r, c);
                var cell    = ws.Cell(r + 1, c + 1);
                cell.Value  = text;
                if (r == 0) { cell.Style.Font.Bold = true;
                              cell.Style.Fill.BackgroundColor = XLColor.LightSteelBlue; }
            }

            ws.Columns().AdjustToContents();
            wb.SaveAs(outputPath);

            return new ScheduleExportResult
            {
                RowCount    = rowCount - 1,
                ColumnCount = colCount,
                FilePath    = outputPath,
            };
        }
    }
}
"""
    files.append(write(out / "ScheduleExportEngine.cs",
        await qwen_fill(engine, "Revit ViewSchedule.GetTableData(), SectionData.GetCellText(row, col)")))

    files.append(write(out / "ScheduleExportCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Microsoft.Win32;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.ReadOnly)]
    [Regeneration(RegenerationOption.Manual)]
    public class ScheduleExportCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc  = data.Application.ActiveUIDocument.Document;
            var view = data.Application.ActiveUIDocument.ActiveView as ViewSchedule;
            if (view == null)
            { TaskDialog.Show("오류", "일람표 뷰에서 실행하세요."); return Result.Cancelled; }

            var dlg = new SaveFileDialog
            {
                Filter   = "Excel 파일 (*.xlsx)|*.xlsx",
                FileName = $"{view.Name}.xlsx",
            };
            if (dlg.ShowDialog() != true) return Result.Cancelled;

            var result = ScheduleExportEngine.Export(view, dlg.FileName);
            TaskDialog.Show("완료",
                $"내보내기 완료\\n행: {result.RowCount}  열: {result.ColumnCount}\\n{result.FilePath}");
            return Result.Succeeded;
        }
    }
}
"""))
    print(f"  [R-10] ScheduleExcelExport — {len(files)}개")
    return files


# R-11  MEP Length Calculator
async def build_r11() -> list[Path]:
    out = REVIT_ROOT / "MEPLengthCalculator"
    out.mkdir(parents=True, exist_ok=True)
    files = []

    engine = """\
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Mechanical;
using Autodesk.Revit.DB.Plumbing;

namespace BIMCommandCenter.Commands
{
    public class MEPLengthGroup
    {
        public string Category    { get; set; }
        public string SystemType  { get; set; }
        public double TotalLengthM { get; set; }
        public int    Count       { get; set; }
    }

    public static class MEPLengthCalculatorEngine
    {
        public static List<MEPLengthGroup> Calculate(Document doc, View view = null)
        {
            var groups = new Dictionary<string, MEPLengthGroup>();
            double feetToM = 0.3048;

            void AddLength(string cat, string sys, double lenFt)
            {
                string key = $"{cat}|{sys}";
                if (!groups.TryGetValue(key, out var g))
                    groups[key] = g = new MEPLengthGroup { Category = cat, SystemType = sys };
                g.TotalLengthM += lenFt * feetToM;
                g.Count++;
            }

            // QWEN_FILL: Pipe, Duct, Conduit, CableTray 각각 collector 로 수집,
            // MEPSystem.Name 또는 파라미터로 시스템 구분, Curve.Length 로 길이 집계
            var collector = view != null
                ? new FilteredElementCollector(doc, view.Id)
                : new FilteredElementCollector(doc);

            // 배관
            foreach (var pipe in collector.OfClass(typeof(Pipe)).Cast<Pipe>())
                AddLength("배관", pipe.get_Parameter(BuiltInParameter.RBS_PIPING_SYSTEM_TYPE_PARAM)?.AsValueString() ?? "", pipe.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH)?.AsDouble() ?? 0);

            // 덕트
            foreach (var duct in new FilteredElementCollector(doc).OfClass(typeof(Duct)).Cast<Duct>())
                AddLength("덕트", duct.get_Parameter(BuiltInParameter.RBS_DUCT_SYSTEM_TYPE_PARAM)?.AsValueString() ?? "", duct.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH)?.AsDouble() ?? 0);

            // 전선관
            foreach (var cond in new FilteredElementCollector(doc).OfClass(typeof(Conduit)).Cast<Conduit>())
                AddLength("전선관", "", cond.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH)?.AsDouble() ?? 0);

            return groups.Values.OrderBy(g => g.Category).ThenBy(g => g.SystemType).ToList();
        }
    }
}
"""
    files.append(write(out / "MEPLengthCalculatorEngine.cs",
        await qwen_fill(engine, "Revit Pipe, Duct, Conduit classes, BuiltInParameter.CURVE_ELEM_LENGTH, RBS_PIPING_SYSTEM_TYPE_PARAM")))

    files.append(write(out / "MEPLengthCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.ReadOnly)]
    [Regeneration(RegenerationOption.Manual)]
    public class MEPLengthCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc    = data.Application.ActiveUIDocument.Document;
            var groups = MEPLengthCalculatorEngine.Calculate(doc);
            var win    = new MEPLengthWindow(groups);
            win.ShowDialog();
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "MEPLengthWindow.xaml.cs", """\
using System.Collections.Generic;
using System.IO;
using System.Windows;
using ClosedXML.Excel;

namespace BIMCommandCenter.Commands
{
    public partial class MEPLengthWindow : Window
    {
        private readonly List<MEPLengthGroup> _groups;
        public MEPLengthWindow(List<MEPLengthGroup> groups)
        {
            _groups = groups;
            InitializeComponent();
            DgGroups.ItemsSource = groups;
        }
        private void BtnExport_Click(object s, RoutedEventArgs e)
        {
            var dlg = new Microsoft.Win32.SaveFileDialog { Filter = "Excel|*.xlsx", FileName = "MEP_Length.xlsx" };
            if (dlg.ShowDialog() != true) return;
            using var wb = new XLWorkbook();
            var ws = wb.Worksheets.Add("MEP 길이");
            ws.Cell(1,1).Value="공종"; ws.Cell(1,2).Value="시스템"; ws.Cell(1,3).Value="길이(m)"; ws.Cell(1,4).Value="개수";
            ws.Row(1).Style.Font.Bold = true;
            for (int i = 0; i < _groups.Count; i++)
            {
                ws.Cell(i+2,1).Value = _groups[i].Category;
                ws.Cell(i+2,2).Value = _groups[i].SystemType;
                ws.Cell(i+2,3).Value = System.Math.Round(_groups[i].TotalLengthM, 2);
                ws.Cell(i+2,4).Value = _groups[i].Count;
            }
            ws.Columns().AdjustToContents();
            wb.SaveAs(dlg.FileName);
            MessageBox.Show($"저장: {dlg.FileName}");
        }
        private void BtnClose_Click(object s, RoutedEventArgs e) => Close();
    }
}
"""))

    files.append(write(out / "MEPLengthWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.MEPLengthWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="MEP Length Calculator" Height="400" Width="500"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="8">
        <Grid.RowDefinitions><RowDefinition Height="*"/><RowDefinition Height="Auto"/></Grid.RowDefinitions>
        <DataGrid x:Name="DgGroups" Grid.Row="0" AutoGenerateColumns="False" IsReadOnly="True" Margin="0,0,0,8">
            <DataGrid.Columns>
                <DataGridTextColumn Header="공종"      Binding="{Binding Category}"                         Width="80"/>
                <DataGridTextColumn Header="시스템"     Binding="{Binding SystemType}"                       Width="*"/>
                <DataGridTextColumn Header="길이(m)"   Binding="{Binding TotalLengthM, StringFormat={}{0:F2}}" Width="90"/>
                <DataGridTextColumn Header="개수"      Binding="{Binding Count}"                            Width="60"/>
            </DataGrid.Columns>
        </DataGrid>
        <StackPanel Grid.Row="1" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="엑셀 저장" Width="90" Margin="4,0" Click="BtnExport_Click"/>
            <Button Content="닫기"      Width="70" Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [R-11] MEPLengthCalculator — {len(files)}개")
    return files


# R-12  Warning Manager
async def build_r12() -> list[Path]:
    out = REVIT_ROOT / "WarningManager"
    out.mkdir(parents=True, exist_ok=True)
    files = []

    engine = """\
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public class WarningGroup
    {
        public string Description { get; set; }
        public int    Count       { get; set; }
        public List<ElementId> ElementIds { get; } = new();
    }

    public static class WarningManagerEngine
    {
        public static List<WarningGroup> Audit(Document doc)
        {
            // QWEN_FILL: doc.GetWarnings() 로 FailureMessage 목록 수집,
            // GetDescriptionText() 로 그룹화, GetFailingElements() 로 요소 ID 수집
            var dict = new Dictionary<string, WarningGroup>();
            foreach (var w in doc.GetWarnings())
            {
                string key = w.GetDescriptionText();
                if (key.Length > 80) key = key.Substring(0, 80);
                if (!dict.TryGetValue(key, out var g))
                    dict[key] = g = new WarningGroup { Description = key };
                g.Count++;
                foreach (var id in w.GetFailingElements())
                    if (!g.ElementIds.Contains(id)) g.ElementIds.Add(id);
            }
            return dict.Values.OrderByDescending(g => g.Count).ToList();
        }
    }
}
"""
    files.append(write(out / "WarningManagerEngine.cs",
        await qwen_fill(engine, "Revit doc.GetWarnings() IList<FailureMessage>, FailureMessage.GetDescriptionText(), GetFailingElements()")))

    files.append(write(out / "WarningManagerCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.ReadOnly)]
    [Regeneration(RegenerationOption.Manual)]
    public class WarningManagerCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var uiDoc  = data.Application.ActiveUIDocument;
            var groups = WarningManagerEngine.Audit(uiDoc.Document);
            var win    = new WarningManagerWindow(groups, uiDoc);
            win.ShowDialog();
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "WarningManagerWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    public partial class WarningManagerWindow : Window
    {
        private readonly UIDocument _uiDoc;
        public WarningManagerWindow(List<WarningGroup> groups, UIDocument uiDoc)
        {
            _uiDoc = uiDoc;
            InitializeComponent();
            DgWarnings.ItemsSource = groups;
            TxtTotal.Text = $"총 경고: {groups.Sum(g => g.Count)}건 / {groups.Count}유형";
        }
        private void BtnIsolate_Click(object s, RoutedEventArgs e)
        {
            if (DgWarnings.SelectedItem is not WarningGroup g) return;
            _uiDoc.Selection.SetElementIds(g.ElementIds);
            TxtStatus.Text = $"'{g.Description.Substring(0,System.Math.Min(40,g.Description.Length))}...' {g.ElementIds.Count}개 선택";
        }
        private void BtnClose_Click(object s, RoutedEventArgs e) => Close();
    }
}
"""))

    files.append(write(out / "WarningManagerWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.WarningManagerWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Warning Manager" Height="440" Width="620"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="8">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <TextBlock Grid.Row="0" x:Name="TxtTotal" FontWeight="Bold" Margin="0,0,0,6"/>
        <DataGrid Grid.Row="1" x:Name="DgWarnings" AutoGenerateColumns="False"
                  IsReadOnly="True" SelectionMode="Single" Margin="0,0,0,8">
            <DataGrid.Columns>
                <DataGridTextColumn Header="경고 유형" Binding="{Binding Description}" Width="*"/>
                <DataGridTextColumn Header="건수"      Binding="{Binding Count}"       Width="60"/>
                <DataGridTextColumn Header="요소 수"   Binding="{Binding ElementIds.Count}" Width="70"/>
            </DataGrid.Columns>
        </DataGrid>
        <TextBlock Grid.Row="2" x:Name="TxtStatus" Margin="0,0,0,6" Foreground="DarkBlue"/>
        <StackPanel Grid.Row="3" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="요소 선택·격리" Width="110" Margin="4,0" Click="BtnIsolate_Click"/>
            <Button Content="닫기"           Width="70"  Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [R-12] WarningManager — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# Navisworks 추가 — Korean Report Common Layer
# ═════════════════════════════════════════════════════════════════
async def build_n04_korean_report() -> list[Path]:
    out = NAV_ROOT / "_Shared" / "KoreanReport"
    out.mkdir(parents=True, exist_ok=True)
    files = []

    files.append(write(out / "KoreanReportGenerator.cs", """\
using System;
using System.Collections.Generic;
using ClosedXML.Excel;

namespace NavisworksShared
{
    /// <summary>모든 Navisworks 애드인 공통 한글 엑셀 리포트 생성기</summary>
    public static class KoreanReportGenerator
    {
        public static string GenerateExcel(
            string sheetTitle,
            string[] headers,
            List<string[]> rows,
            string outputPath,
            string projectName = "")
        {
            using var wb = new XLWorkbook();
            var ws = wb.Worksheets.Add(sheetTitle.Length > 31
                ? sheetTitle.Substring(0, 31) : sheetTitle);

            // 타이틀 행
            int startRow = 1;
            if (!string.IsNullOrEmpty(projectName))
            {
                ws.Cell(1, 1).Value = $"프로젝트: {projectName}";
                ws.Cell(2, 1).Value = $"생성일시: {DateTime.Now:yyyy-MM-dd HH:mm}";
                ws.Range(1, 1, 1, headers.Length).Merge();
                ws.Range(2, 1, 2, headers.Length).Merge();
                ws.Row(1).Style.Font.Bold = true;
                ws.Row(1).Style.Fill.BackgroundColor = XLColor.DarkSlateBlue;
                ws.Row(1).Style.Font.FontColor = XLColor.White;
                startRow = 3;
            }

            // 헤더
            for (int c = 0; c < headers.Length; c++)
            {
                var cell = ws.Cell(startRow, c + 1);
                cell.Value = headers[c];
                cell.Style.Font.Bold = true;
                cell.Style.Fill.BackgroundColor = XLColor.SteelBlue;
                cell.Style.Font.FontColor = XLColor.White;
                cell.Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;
            }

            // 데이터
            for (int r = 0; r < rows.Count; r++)
            {
                var row = rows[r];
                for (int c = 0; c < row.Length && c < headers.Length; c++)
                    ws.Cell(startRow + r + 1, c + 1).Value = row[c];
                if (r % 2 == 1)
                    ws.Row(startRow + r + 1).Style.Fill.BackgroundColor = XLColor.AliceBlue;
            }

            // 요약 행
            ws.Cell(startRow + rows.Count + 1, 1).Value = $"합계: {rows.Count}건";
            ws.Cell(startRow + rows.Count + 1, 1).Style.Font.Bold = true;

            ws.Columns().AdjustToContents();
            ws.SheetView.FreezeRows(startRow);
            wb.SaveAs(outputPath);
            return outputPath;
        }

        public static string GenerateSummarySheet(
            string sheetTitle, Dictionary<string, int> summary, string outputPath)
        {
            var rows = new List<string[]>();
            foreach (var kv in summary)
                rows.Add(new[] { kv.Key, kv.Value.ToString() });
            return GenerateExcel(sheetTitle, new[] { "항목", "건수" }, rows, outputPath);
        }
    }
}
"""))

    files.append(write(out / "NavisworksHelper.cs", """\
using Autodesk.Navisworks.Api;

namespace NavisworksShared
{
    /// <summary>Navisworks 애드인 공통 유틸리티</summary>
    public static class NavisworksHelper
    {
        public static string GetLayerName(ModelItem item)
        {
            try
            {
                return item?.AncestorsAndSelf.FindFirstObjectAncestor()
                    ?.DisplayName ?? "Unknown";
            }
            catch { return "Unknown"; }
        }

        public static string GetFileName(ModelItem item)
        {
            try
            {
                var model = item?.Model;
                return model != null
                    ? System.IO.Path.GetFileNameWithoutExtension(model.FileName)
                    : "Unknown";
            }
            catch { return "Unknown"; }
        }

        public static bool IsModelOpen()
        {
            var doc = Application.ActiveDocument;
            return doc != null && doc.Models.Count > 0;
        }
    }
}
"""))
    print(f"  [N-04] KoreanReport CommonLayer — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# 메인
# ═════════════════════════════════════════════════════════════════
async def main():
    require_addin_dev_source_root()
    print(f"BCC Add-in 2차 개발 러너 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")

    batches = [
        # ① 누락 UI 완성
        ("UI-R04", "ElementRenumbering XAML",      "Revit",      missing_r04_ui),
        ("UI-R05", "ProjectCleanup Window",         "Revit",      missing_r05_ui),
        ("UI-N01", "ClashBoard WinForm",            "Navisworks", missing_n01_ui),
        ("UI-N02", "ClashGroup WinForm",            "Navisworks", missing_n02_ui),
        ("UI-N03", "ClashTestDefiner WinForm",      "Navisworks", missing_n03_ui),
        # ② Phase 2 Revit
        ("R-06",   "Line Cleanup Lite",             "Revit",      build_r06),
        ("R-07",   "Smart Selector Lite",           "Revit",      build_r07),
        ("R-08",   "Workset Inspector Lite",        "Revit",      build_r08),
        ("R-09",   "Link Health & Reload",          "Revit",      build_r09),
        ("R-10",   "Schedule Excel Export",         "Revit",      build_r10),
        ("R-11",   "MEP Length Calculator",         "Revit",      build_r11),
        ("R-12",   "Warning Manager",               "Revit",      build_r12),
        # ③ Navisworks 공통 레이어
        ("N-04",   "Korean Report Common Layer",    "Navisworks", build_n04_korean_report),
    ]

    for item_id, display, kind, builder in batches:
        print(f"\n{'='*55}\n[{item_id}] {display}\n{'='*55}")
        files = await builder()
        if files:
            mail(item_id, display, kind, files)
            print(f"  ✓ 이메일 발송")

    print(f"\n\n2차 개발 전체 완료")


if __name__ == "__main__":
    asyncio.run(main())
