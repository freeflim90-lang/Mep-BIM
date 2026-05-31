#!/usr/bin/env python3
"""BIM Command Center Add-in 개발 자동화 러너

전략:
  - Claude가 직접 완전한 C# 스캐폴드(컴파일 가능한 뼈대) 작성
  - Qwen Coder는 각 메서드의 Revit/Navisworks API 로직 본문만 채움
  - 파일 저장 후 이메일 발송

실행: python3 scripts/bcc_addin_dev_runner.py
"""
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


# ─────────────────────────────────────────────────────────────────
# 헬퍼: Qwen으로 메서드 본문만 채우기
# ─────────────────────────────────────────────────────────────────
async def qwen_fill(placeholder_code: str, hint: str) -> str:
    """스캐폴드에서 // QWEN_FILL 마커를 Qwen 로직으로 교체."""
    if "// QWEN_FILL" not in placeholder_code:
        return placeholder_code

    prompt = f"""다음 C# 코드에서 `// QWEN_FILL` 주석 부분을 실제 구현으로 채워라.
Revit/Navisworks API를 정확히 사용하고, 한국어 주석 포함, 컴파일 가능하게 완성하라.

힌트: {hint}

```csharp
{placeholder_code}
```

완성된 전체 코드를 ```csharp 블록으로 반환:"""

    try:
        async with httpx.AsyncClient(timeout=180) as client:
            r = await client.post(f"{OLLAMA_URL}/api/generate",
                json={"model": CODER_MODEL, "prompt": prompt, "stream": False,
                      "options": {"temperature": 0.1, "num_predict": 3000}})
            r.raise_for_status()
        response = r.json().get("response", "")
        m = re.search(r"```(?:csharp|cs)?\s*([\s\S]+?)```", response)
        return m.group(1).strip() if m else placeholder_code
    except Exception as e:
        print(f"    Qwen 오류 ({e}) — 스캐폴드 그대로 사용")
        return placeholder_code


def send_email(item_id: str, display: str, addon_type: str, files: list[Path]) -> None:
    subject = f"[BCC 개발완료] {item_id} {display}"
    lines = [
        f"BIM Command Center Add-in 스캐폴드 생성 완료",
        f"아이템  : {item_id} — {display}",
        f"타입    : {addon_type}",
        f"생성일시 : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "생성 파일:",
    ]
    for f in files:
        lines.append(f"  {f.name}  ({f.stat().st_size:,} bytes)")
    lines += ["", "개발 PC에서 빌드 후 BIM Command Center 리본에 등록하세요.",
              "각 파일의 // QWEN_FILL 마커가 있다면 Qwen이 로직을 채운 상태입니다."]
    result = send_gmail(subject=subject, body="\n".join(lines), attachments=files)
    print(f"  이메일: {result}")


# ═════════════════════════════════════════════════════════════════
#  R-01  Tag / Text Aligner
# ═════════════════════════════════════════════════════════════════
async def build_r01() -> list[Path]:
    out = REVIT_ROOT / "TagTextAligner"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    # ── TagTextAlignerEngine.cs ───────────────────────────────────
    engine = """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    /// <summary>태그·문자 정렬 로직 (순수 연산, UI 없음)</summary>
    public enum AlignMode { Left, Right, Top, Bottom, DistributeH, DistributeV }

    public static class TagTextAlignerEngine
    {
        /// <summary>선택 요소 중 정렬 대상만 필터링 (IndependentTag, TextNote, 핀 제외)</summary>
        public static List<Element> FilterTargets(ICollection<ElementId> ids, Document doc)
        {
            // QWEN_FILL: ids 에서 IndependentTag 또는 TextNote 이고 IsPinned==false 인 것만 반환
            var result = new List<Element>();
            foreach (var id in ids)
            {
                var el = doc.GetElement(id);
                if (el == null) continue;
                if (el is IndependentTag tag && !tag.Pinned)  result.Add(el);
                else if (el is TextNote tn && !tn.Pinned)     result.Add(el);
            }
            return result;
        }

        /// <summary>정렬 미리보기: 이동 후 예상 좌표 반환 (트랜잭션 없음)</summary>
        public static Dictionary<ElementId, XYZ> Preview(List<Element> targets, AlignMode mode)
        {
            // QWEN_FILL: mode 에 따라 각 요소의 Location.Point 를 정렬/배분한 결과 좌표 계산
            var result = new Dictionary<ElementId, XYZ>();
            if (targets.Count == 0) return result;

            var points = targets.Select(e => ((LocationPoint)e.Location).Point).ToList();

            switch (mode)
            {
                case AlignMode.Left:
                    double minX = points.Min(p => p.X);
                    for (int i = 0; i < targets.Count; i++)
                        result[targets[i].Id] = new XYZ(minX, points[i].Y, points[i].Z);
                    break;
                case AlignMode.Right:
                    double maxX = points.Max(p => p.X);
                    for (int i = 0; i < targets.Count; i++)
                        result[targets[i].Id] = new XYZ(maxX, points[i].Y, points[i].Z);
                    break;
                case AlignMode.Top:
                    double maxY = points.Max(p => p.Y);
                    for (int i = 0; i < targets.Count; i++)
                        result[targets[i].Id] = new XYZ(points[i].X, maxY, points[i].Z);
                    break;
                case AlignMode.Bottom:
                    double minY = points.Min(p => p.Y);
                    for (int i = 0; i < targets.Count; i++)
                        result[targets[i].Id] = new XYZ(points[i].X, minY, points[i].Z);
                    break;
                case AlignMode.DistributeH:
                    var sortedH = targets.OrderBy(e => ((LocationPoint)e.Location).Point.X).ToList();
                    var ptsH    = sortedH.Select(e => ((LocationPoint)e.Location).Point).ToList();
                    double spanX = ptsH.Last().X - ptsH.First().X;
                    double stepX = sortedH.Count > 1 ? spanX / (sortedH.Count - 1) : 0;
                    for (int i = 0; i < sortedH.Count; i++)
                        result[sortedH[i].Id] = new XYZ(ptsH[0].X + stepX * i, ptsH[i].Y, ptsH[i].Z);
                    break;
                case AlignMode.DistributeV:
                    var sortedV = targets.OrderBy(e => ((LocationPoint)e.Location).Point.Y).ToList();
                    var ptsV    = sortedV.Select(e => ((LocationPoint)e.Location).Point).ToList();
                    double spanY = ptsV.Last().Y - ptsV.First().Y;
                    double stepY = sortedV.Count > 1 ? spanY / (sortedV.Count - 1) : 0;
                    for (int i = 0; i < sortedV.Count; i++)
                        result[sortedV[i].Id] = new XYZ(ptsV[i].X, ptsV[0].Y + stepY * i, ptsV[i].Z);
                    break;
            }
            return result;
        }

        /// <summary>트랜잭션 내 실제 이동 (호출 전 트랜잭션 시작 필요)</summary>
        public static int Apply(Document doc, Dictionary<ElementId, XYZ> moves)
        {
            int count = 0;
            foreach (var kv in moves)
            {
                var el = doc.GetElement(kv.Key);
                if (el?.Location is LocationPoint lp)
                {
                    lp.Point = kv.Value;
                    count++;
                }
            }
            return count;
        }
    }
}
"""
    p = out / "TagTextAlignerEngine.cs"
    p.write_text(engine, encoding="utf-8")
    files.append(p)

    # ── TagTextAlignerCommand.cs ──────────────────────────────────
    command = """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using BIMCommandCenter.Commands;
using System;
using System.Windows;

namespace BIMCommandCenter.Commands
{
    /// <summary>BIM Command Center — Tag/Text Aligner 진입점</summary>
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class TagTextAlignerCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            UIDocument uiDoc = commandData.Application.ActiveUIDocument;
            Document   doc   = uiDoc.Document;

            // 선택 요소 가져오기
            var selIds  = uiDoc.Selection.GetElementIds();
            var targets = TagTextAlignerEngine.FilterTargets(selIds, doc);

            if (targets.Count < 2)
            {
                TaskDialog.Show("Tag/Text Aligner",
                    "정렬할 태그 또는 문자를 2개 이상 선택하세요.\n(핀된 주석은 제외됩니다)");
                return Result.Cancelled;
            }

            // WPF 창 표시
            var window = new TagTextAlignerWindow(targets.Count);
            if (window.ShowDialog() != true) return Result.Cancelled;

            // 미리보기 계산
            var moves = TagTextAlignerEngine.Preview(targets, window.SelectedMode);

            // 트랜잭션 실행
            using (var tx = new Transaction(doc, "BCC - Tag/Text Align"))
            {
                tx.Start();
                int moved = TagTextAlignerEngine.Apply(doc, moves);
                tx.Commit();
                TaskDialog.Show("Tag/Text Aligner", $"{moved}개 주석을 정렬했습니다.");
            }

            return Result.Succeeded;
        }
    }
}
"""
    p = out / "TagTextAlignerCommand.cs"
    p.write_text(command, encoding="utf-8")
    files.append(p)

    # ── TagTextAlignerWindow.xaml.cs ──────────────────────────────
    window = """\
using System.Windows;
using BIMCommandCenter.Commands;

namespace BIMCommandCenter.Commands
{
    /// <summary>정렬 모드 선택 WPF 다이얼로그</summary>
    public partial class TagTextAlignerWindow : Window
    {
        public AlignMode SelectedMode { get; private set; }
        private readonly int _count;

        public TagTextAlignerWindow(int count)
        {
            _count = count;
            InitializeComponent();
            TitleText.Text = $"선택된 주석: {_count}개";
        }

        private void BtnLeft_Click(object s, RoutedEventArgs e)    { SelectedMode = AlignMode.Left;        DialogResult = true; }
        private void BtnRight_Click(object s, RoutedEventArgs e)   { SelectedMode = AlignMode.Right;       DialogResult = true; }
        private void BtnTop_Click(object s, RoutedEventArgs e)     { SelectedMode = AlignMode.Top;         DialogResult = true; }
        private void BtnBottom_Click(object s, RoutedEventArgs e)  { SelectedMode = AlignMode.Bottom;      DialogResult = true; }
        private void BtnDistH_Click(object s, RoutedEventArgs e)   { SelectedMode = AlignMode.DistributeH; DialogResult = true; }
        private void BtnDistV_Click(object s, RoutedEventArgs e)   { SelectedMode = AlignMode.DistributeV; DialogResult = true; }
        private void BtnCancel_Click(object s, RoutedEventArgs e)  { DialogResult = false; }
    }
}
"""
    p = out / "TagTextAlignerWindow.xaml.cs"
    p.write_text(window, encoding="utf-8")
    files.append(p)

    # ── TagTextAlignerWindow.xaml ─────────────────────────────────
    xaml = """\
<Window x:Class="BIMCommandCenter.Commands.TagTextAlignerWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Tag / Text Aligner" Height="220" Width="320"
        ResizeMode="NoResize" WindowStartupLocation="CenterScreen">
    <StackPanel Margin="16">
        <TextBlock x:Name="TitleText" FontWeight="Bold" Margin="0,0,0,12"/>
        <UniformGrid Columns="3" Rows="2">
            <Button Content="← 왼쪽 정렬"  Click="BtnLeft_Click"   Margin="2" Padding="6"/>
            <Button Content="→ 오른쪽 정렬" Click="BtnRight_Click"  Margin="2" Padding="6"/>
            <Button Content="↑ 위 정렬"    Click="BtnTop_Click"    Margin="2" Padding="6"/>
            <Button Content="↓ 아래 정렬"  Click="BtnBottom_Click" Margin="2" Padding="6"/>
            <Button Content="⟺ 가로 균등"  Click="BtnDistH_Click"  Margin="2" Padding="6"/>
            <Button Content="↕ 세로 균등"  Click="BtnDistV_Click"  Margin="2" Padding="6"/>
        </UniformGrid>
        <Button Content="취소" Click="BtnCancel_Click" Margin="2,12,2,0" Padding="6"/>
    </StackPanel>
</Window>
"""
    p = out / "TagTextAlignerWindow.xaml"
    p.write_text(xaml, encoding="utf-8")
    files.append(p)

    print(f"  [R-01] TagTextAligner — {len(files)}개 파일 저장")
    return files


# ═════════════════════════════════════════════════════════════════
#  R-02  View Template Copier
# ═════════════════════════════════════════════════════════════════
async def build_r02() -> list[Path]:
    out = REVIT_ROOT / "ViewTemplateCopier"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    engine_scaffold = """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public enum CollisionPolicy { Skip, Rename, Replace }

    public class TemplateCopyResult
    {
        public int Copied  { get; set; }
        public int Skipped { get; set; }
        public int Renamed { get; set; }
        public List<string> Log { get; } = new List<string>();
    }

    /// <summary>뷰 템플릿 복사 엔진</summary>
    public static class ViewTemplateCopierEngine
    {
        /// <summary>문서에서 뷰 템플릿 목록 반환</summary>
        public static List<View> GetTemplates(Document doc)
        {
            // QWEN_FILL: FilteredElementCollector로 IsTemplate==true 인 View 목록 반환
            return new FilteredElementCollector(doc)
                .OfClass(typeof(View))
                .Cast<View>()
                .Where(v => v.IsTemplate)
                .OrderBy(v => v.Name)
                .ToList();
        }

        /// <summary>Dry-run: 복사 예상 결과 텍스트 반환 (실제 변경 없음)</summary>
        public static TemplateCopyResult DryRun(
            Document source, Document target,
            IEnumerable<string> templateNames, CollisionPolicy policy)
        {
            var result  = new TemplateCopyResult();
            var existing = GetTemplates(target).Select(v => v.Name).ToHashSet();

            foreach (var name in templateNames)
            {
                if (existing.Contains(name))
                {
                    switch (policy)
                    {
                        case CollisionPolicy.Skip:
                            result.Skipped++;
                            result.Log.Add($"SKIP: '{name}' (이미 존재)");
                            break;
                        case CollisionPolicy.Rename:
                            result.Renamed++;
                            result.Log.Add($"RENAME: '{name}' → '{name}_복사'");
                            break;
                        case CollisionPolicy.Replace:
                            result.Copied++;
                            result.Log.Add($"REPLACE: '{name}' (덮어쓰기 예정)");
                            break;
                    }
                }
                else
                {
                    result.Copied++;
                    result.Log.Add($"COPY: '{name}'");
                }
            }
            return result;
        }

        /// <summary>실제 복사 실행 (트랜잭션 내부에서 호출)</summary>
        public static TemplateCopyResult Execute(
            Document source, Document target,
            IEnumerable<string> templateNames, CollisionPolicy policy)
        {
            // QWEN_FILL: source 에서 templateNames 에 해당하는 View 요소를
            // ElementTransformUtils.CopyElements 또는 Document.Copy 로 target 에 복사.
            // policy 에 따라 충돌 처리. TemplateCopyResult 반환.
            var result   = new TemplateCopyResult();
            var srcTemps = GetTemplates(source).ToDictionary(v => v.Name);
            var existing = GetTemplates(target).Select(v => v.Name).ToHashSet();

            foreach (var name in templateNames)
            {
                if (!srcTemps.TryGetValue(name, out var srcView)) continue;

                if (existing.Contains(name))
                {
                    if (policy == CollisionPolicy.Skip)
                    { result.Skipped++; result.Log.Add($"SKIP: '{name}'"); continue; }
                }

                try
                {
                    var ids = new List<ElementId> { srcView.Id };
                    ElementTransformUtils.CopyElements(source, ids, target, Transform.Identity,
                        new CopyPasteOptions());
                    result.Copied++;
                    result.Log.Add($"OK: '{name}'");
                }
                catch (Exception ex)
                {
                    result.Log.Add($"ERR: '{name}' — {ex.Message}");
                }
            }
            return result;
        }
    }
}
"""
    scaffold = await qwen_fill(engine_scaffold,
        "Revit FilteredElementCollector, ElementTransformUtils.CopyElements 사용법")
    p = out / "ViewTemplateCopierEngine.cs"
    p.write_text(scaffold, encoding="utf-8")
    files.append(p)

    command = """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    /// <summary>BIM Command Center — View Template Copier 진입점</summary>
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class ViewTemplateCopierCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            var uiApp = commandData.Application;
            var docs   = new System.Collections.Generic.List<Document>();
            foreach (Document d in uiApp.Application.Documents) docs.Add(d);

            var win = new ViewTemplateCopierWindow(docs);
            if (win.ShowDialog() != true) return Result.Cancelled;

            // Dry-run 확인
            var dry = ViewTemplateCopierEngine.DryRun(
                win.SourceDocument, win.TargetDocument,
                win.SelectedTemplateNames, win.Policy);

            string preview = string.Join("\\n", dry.Log);
            var td = new TaskDialog("View Template Copier - 미리보기");
            td.MainContent  = $"복사: {dry.Copied}  스킵: {dry.Skipped}  변경: {dry.Renamed}\\n\\n{preview}";
            td.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel;
            if (td.Show() != TaskDialogResult.Ok) return Result.Cancelled;

            using (var tx = new Transaction(win.TargetDocument, "BCC - Copy View Templates"))
            {
                tx.Start();
                var result = ViewTemplateCopierEngine.Execute(
                    win.SourceDocument, win.TargetDocument,
                    win.SelectedTemplateNames, win.Policy);
                tx.Commit();
                TaskDialog.Show("완료",
                    $"복사: {result.Copied}  스킵: {result.Skipped}");
            }
            return Result.Succeeded;
        }
    }
}
"""
    p = out / "ViewTemplateCopierCommand.cs"
    p.write_text(command, encoding="utf-8")
    files.append(p)

    window_cs = """\
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    /// <summary>소스 문서·템플릿 선택 + 충돌 정책 WPF 창</summary>
    public partial class ViewTemplateCopierWindow : Window
    {
        private readonly List<Document> _docs;
        public Document   SourceDocument      { get; private set; }
        public Document   TargetDocument      { get; private set; }
        public List<string> SelectedTemplateNames { get; private set; } = new();
        public CollisionPolicy Policy         { get; private set; } = CollisionPolicy.Skip;

        public ViewTemplateCopierWindow(List<Document> docs)
        {
            _docs = docs;
            InitializeComponent();
            CboSource.ItemsSource = docs.Select(d => d.Title).ToList();
            CboTarget.ItemsSource = docs.Select(d => d.Title).ToList();
            CboPolicy.ItemsSource = new[] { "스킵(기본)", "이름 변경", "덮어쓰기" };
            CboPolicy.SelectedIndex = 0;
        }

        private void CboSource_SelectionChanged(object s, SelectionChangedEventArgs e)
        {
            SourceDocument = _docs[CboSource.SelectedIndex];
            LstTemplates.ItemsSource = ViewTemplateCopierEngine
                .GetTemplates(SourceDocument).Select(v => v.Name).ToList();
        }

        private void BtnOk_Click(object s, RoutedEventArgs e)
        {
            if (CboTarget.SelectedIndex < 0) { MessageBox.Show("대상 문서를 선택하세요."); return; }
            TargetDocument        = _docs[CboTarget.SelectedIndex];
            SelectedTemplateNames = LstTemplates.SelectedItems.Cast<string>().ToList();
            Policy = CboPolicy.SelectedIndex switch { 1 => CollisionPolicy.Rename, 2 => CollisionPolicy.Replace, _ => CollisionPolicy.Skip };
            if (SelectedTemplateNames.Count == 0) { MessageBox.Show("템플릿을 선택하세요."); return; }
            DialogResult = true;
        }
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }
}
"""
    p = out / "ViewTemplateCopierWindow.xaml.cs"
    p.write_text(window_cs, encoding="utf-8")
    files.append(p)

    xaml = """\
<Window x:Class="BIMCommandCenter.Commands.ViewTemplateCopierWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="View Template Copier" Height="380" Width="420"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="12">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <StackPanel Grid.Row="0" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="소스 문서:" Width="80" VerticalAlignment="Center"/>
            <ComboBox x:Name="CboSource" Width="280" SelectionChanged="CboSource_SelectionChanged"/>
        </StackPanel>
        <StackPanel Grid.Row="1" Orientation="Horizontal" Margin="0,0,0,6">
            <TextBlock Text="대상 문서:" Width="80" VerticalAlignment="Center"/>
            <ComboBox x:Name="CboTarget" Width="280"/>
        </StackPanel>
        <ListBox x:Name="LstTemplates" Grid.Row="2" SelectionMode="Multiple" Margin="0,0,0,6"/>
        <StackPanel Grid.Row="3" Orientation="Horizontal" Margin="0,0,0,8">
            <TextBlock Text="충돌 정책:" Width="80" VerticalAlignment="Center"/>
            <ComboBox x:Name="CboPolicy" Width="140"/>
        </StackPanel>
        <StackPanel Grid.Row="4" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="실행" Width="80" Margin="4,0" Click="BtnOk_Click"/>
            <Button Content="취소" Width="80" Click="BtnCancel_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""
    p = out / "ViewTemplateCopierWindow.xaml"
    p.write_text(xaml, encoding="utf-8")
    files.append(p)

    print(f"  [R-02] ViewTemplateCopier — {len(files)}개 파일 저장")
    return files


# ═════════════════════════════════════════════════════════════════
#  R-03  Type Batch Definer
# ═════════════════════════════════════════════════════════════════
async def build_r03() -> list[Path]:
    out = REVIT_ROOT / "TypeBatchDefiner"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    model_cs = """\
using System.Collections.Generic;
using Newtonsoft.Json;

namespace BIMCommandCenter.Commands
{
    /// <summary>타입 정의 JSON 데이터 모델</summary>
    public class TypeDefinition
    {
        [JsonProperty("familyName")]  public string FamilyName  { get; set; }
        [JsonProperty("typeName")]    public string TypeName    { get; set; }
        [JsonProperty("parameters")]  public Dictionary<string, object> Parameters { get; set; } = new();
    }

    public class TypeDefResult
    {
        public int Created  { get; set; }
        public int Skipped  { get; set; }
        public int Errors   { get; set; }
        public List<string> Log { get; } = new List<string>();
    }
}
"""
    p = out / "TypeDefinition.cs"
    p.write_text(model_cs, encoding="utf-8")
    files.append(p)

    engine_scaffold = """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Revit.DB;
using Newtonsoft.Json;

namespace BIMCommandCenter.Commands
{
    /// <summary>타입 일괄 생성 엔진</summary>
    public static class TypeBatchDefinerEngine
    {
        public static List<TypeDefinition> LoadJson(string jsonPath)
            => JsonConvert.DeserializeObject<List<TypeDefinition>>(File.ReadAllText(jsonPath))
               ?? new List<TypeDefinition>();

        public static TypeDefResult DryRun(Document doc, List<TypeDefinition> defs, bool overwrite)
        {
            var result = new TypeDefResult();
            foreach (var def in defs)
            {
                // QWEN_FILL: doc에서 def.FamilyName 패밀리를 찾아 def.TypeName 타입 존재 여부 확인
                // 없으면 result.Created++, 있고 overwrite=false면 result.Skipped++
                var family = GetFamily(doc, def.FamilyName);
                if (family == null)
                { result.Errors++; result.Log.Add($"패밀리 없음: {def.FamilyName}"); continue; }

                bool exists = FamilyTypeExists(doc, def.FamilyName, def.TypeName);
                if (exists && !overwrite)
                { result.Skipped++; result.Log.Add($"SKIP: {def.FamilyName}/{def.TypeName}"); }
                else
                { result.Created++; result.Log.Add($"CREATE: {def.FamilyName}/{def.TypeName}"); }
            }
            return result;
        }

        public static TypeDefResult Execute(Document doc, List<TypeDefinition> defs, bool overwrite)
        {
            // QWEN_FILL: defs 순서대로
            // 1) GetFamily 로 Family 찾기
            // 2) family.GetFamilySymbolIds() 로 기존 FamilySymbol 찾기
            // 3) 없거나 overwrite 이면 FamilySymbol 복제 후 파라미터 설정
            // 4) symbol.Activate() 호출
            var result = new TypeDefResult();
            foreach (var def in defs)
            {
                try
                {
                    var family = GetFamily(doc, def.FamilyName);
                    if (family == null) { result.Errors++; continue; }

                    FamilySymbol existing = GetFamilySymbol(doc, def.FamilyName, def.TypeName);
                    FamilySymbol symbol;

                    if (existing != null && !overwrite)
                    { result.Skipped++; result.Log.Add($"SKIP: {def.TypeName}"); continue; }

                    if (existing != null)
                        symbol = existing;
                    else
                    {
                        // 첫 번째 심볼 복제
                        var baseId = family.GetFamilySymbolIds().First();
                        var baseSymbol = doc.GetElement(baseId) as FamilySymbol;
                        symbol = baseSymbol.Duplicate(def.TypeName) as FamilySymbol;
                    }

                    if (!symbol.IsActive) symbol.Activate();

                    // 파라미터 설정
                    foreach (var kv in def.Parameters)
                    {
                        var param = symbol.LookupParameter(kv.Key);
                        if (param == null || param.IsReadOnly) continue;
                        SetParameter(param, kv.Value);
                    }
                    result.Created++;
                    result.Log.Add($"OK: {def.FamilyName}/{def.TypeName}");
                }
                catch (Exception ex) { result.Errors++; result.Log.Add($"ERR: {ex.Message}"); }
            }
            return result;
        }

        private static Family GetFamily(Document doc, string name)
            => new FilteredElementCollector(doc).OfClass(typeof(Family))
               .Cast<Family>().FirstOrDefault(f => f.Name == name);

        private static bool FamilyTypeExists(Document doc, string familyName, string typeName)
            => GetFamilySymbol(doc, familyName, typeName) != null;

        private static FamilySymbol GetFamilySymbol(Document doc, string familyName, string typeName)
        {
            // QWEN_FILL: FilteredElementCollector 로 FamilySymbol 검색, family.Name == familyName && symbol.Name == typeName
            return new FilteredElementCollector(doc).OfClass(typeof(FamilySymbol))
                .Cast<FamilySymbol>()
                .FirstOrDefault(s => s.FamilyName == familyName && s.Name == typeName);
        }

        private static void SetParameter(Parameter p, object value)
        {
            if (value is long l)         p.Set(l);
            else if (value is double d)  p.Set(d);
            else if (value is string s)  p.Set(s);
            else if (value is int i)     p.Set(i);
        }
    }
}
"""
    filled = await qwen_fill(engine_scaffold,
        "Revit Family, FamilySymbol API. family.GetFamilySymbolIds(), symbol.Duplicate(name)")
    p = out / "TypeBatchDefinerEngine.cs"
    p.write_text(filled, encoding="utf-8")
    files.append(p)

    command = """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class TypeBatchDefinerCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc = data.Application.ActiveUIDocument.Document;
            var win = new TypeBatchDefinerWindow();
            if (win.ShowDialog() != true) return Result.Cancelled;

            var defs = TypeBatchDefinerEngine.LoadJson(win.JsonPath);
            var dry  = TypeBatchDefinerEngine.DryRun(doc, defs, win.Overwrite);

            var td = new TaskDialog("Type Batch Definer — 미리보기");
            td.MainContent   = $"생성 예정: {dry.Created}  스킵: {dry.Skipped}  오류: {dry.Errors}\n"
                             + string.Join("\n", dry.Log.GetRange(0, System.Math.Min(20, dry.Log.Count)));
            td.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel;
            if (td.Show() != TaskDialogResult.Ok) return Result.Cancelled;

            using (var tx = new Transaction(doc, "BCC - Type Batch Define"))
            {
                tx.Start();
                var r = TypeBatchDefinerEngine.Execute(doc, defs, win.Overwrite);
                tx.Commit();
                TaskDialog.Show("완료", $"생성: {r.Created}  스킵: {r.Skipped}  오류: {r.Errors}");
            }
            return Result.Succeeded;
        }
    }
}
"""
    p = out / "TypeBatchDefinerCommand.cs"
    p.write_text(command, encoding="utf-8")
    files.append(p)

    win_cs = """\
using System.Windows;
using Microsoft.Win32;

namespace BIMCommandCenter.Commands
{
    public partial class TypeBatchDefinerWindow : Window
    {
        public string JsonPath { get; private set; }
        public bool   Overwrite { get; private set; }

        public TypeBatchDefinerWindow() => InitializeComponent();

        private void BtnBrowse_Click(object s, RoutedEventArgs e)
        {
            var dlg = new OpenFileDialog { Filter = "JSON 파일 (*.json)|*.json" };
            if (dlg.ShowDialog() == true) TxtPath.Text = dlg.FileName;
        }
        private void BtnOk_Click(object s, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(TxtPath.Text)) { MessageBox.Show("JSON 파일을 선택하세요."); return; }
            JsonPath  = TxtPath.Text;
            Overwrite = ChkOverwrite.IsChecked == true;
            DialogResult = true;
        }
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }
}
"""
    p = out / "TypeBatchDefinerWindow.xaml.cs"
    p.write_text(win_cs, encoding="utf-8")
    files.append(p)

    xaml = """\
<Window x:Class="BIMCommandCenter.Commands.TypeBatchDefinerWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Type Batch Definer" Height="180" Width="400" ResizeMode="NoResize"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="12">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <StackPanel Grid.Row="0" Orientation="Horizontal" Margin="0,0,0,8">
            <TextBlock Text="JSON 파일:" VerticalAlignment="Center" Width="70"/>
            <TextBox x:Name="TxtPath" Width="220" Margin="4,0"/>
            <Button Content="찾기" Width="50" Click="BtnBrowse_Click"/>
        </StackPanel>
        <CheckBox x:Name="ChkOverwrite" Grid.Row="1" Content="기존 타입 덮어쓰기" Margin="0,0,0,12"/>
        <StackPanel Grid.Row="2" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="Dry-Run 후 실행" Width="110" Margin="4,0" Click="BtnOk_Click"/>
            <Button Content="취소" Width="60" Click="BtnCancel_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""
    p = out / "TypeBatchDefinerWindow.xaml"
    p.write_text(xaml, encoding="utf-8")
    files.append(p)

    print(f"  [R-03] TypeBatchDefiner — {len(files)}개 파일 저장")
    return files


# ═════════════════════════════════════════════════════════════════
#  R-04  Element Renumbering
# ═════════════════════════════════════════════════════════════════
async def build_r04() -> list[Path]:
    out = REVIT_ROOT / "ElementRenumbering"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    rule_cs = """\
namespace BIMCommandCenter.Commands
{
    public enum SortOrder { SelectionOrder, ByX, ByY, ByLevel }

    /// <summary>번호 재배정 규칙 모델</summary>
    public class RenumberRule
    {
        public string CategoryName  { get; set; } = "Rooms";
        public string ParameterName { get; set; } = "Number";
        public string Prefix        { get; set; } = "";
        public int    StartNumber   { get; set; } = 1;
        public int    Increment     { get; set; } = 1;
        public int    Digits        { get; set; } = 0;  // 0 = 자동
        public SortOrder SortBy     { get; set; } = SortOrder.SelectionOrder;
    }

    public class RenumberPreview
    {
        public Autodesk.Revit.DB.ElementId Id { get; set; }
        public string OldNumber { get; set; }
        public string NewNumber { get; set; }
    }
}
"""
    p = out / "RenumberRule.cs"
    p.write_text(rule_cs, encoding="utf-8")
    files.append(p)

    engine_scaffold = """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;

namespace BIMCommandCenter.Commands
{
    /// <summary>요소 번호 재배정 엔진</summary>
    public static class ElementRenumberingEngine
    {
        /// <summary>카테고리명으로 요소 수집 + 정렬 적용</summary>
        public static List<Element> CollectAndSort(Document doc,
            ICollection<ElementId> selection, RenumberRule rule)
        {
            // QWEN_FILL: selection 이 있으면 그것만, 없으면 FilteredElementCollector 로
            // rule.CategoryName 카테고리 전체 수집. rule.SortBy 에 따라 정렬.
            List<Element> elems;
            if (selection != null && selection.Count > 0)
                elems = selection.Select(id => doc.GetElement(id))
                                 .Where(e => e != null).ToList();
            else
            {
                var bic = GetBuiltInCategory(rule.CategoryName);
                elems = bic.HasValue
                    ? new FilteredElementCollector(doc).OfCategory(bic.Value)
                          .WhereElementIsNotElementType().ToList()
                    : new List<Element>();
            }

            return rule.SortBy switch
            {
                SortOrder.ByX     => elems.OrderBy(e => GetPoint(e).X).ToList(),
                SortOrder.ByY     => elems.OrderBy(e => GetPoint(e).Y).ToList(),
                SortOrder.ByLevel => elems.OrderBy(e => (e as Room)?.Level?.Elevation ?? 0)
                                          .ThenBy(e => GetPoint(e).X).ToList(),
                _                 => elems,
            };
        }

        /// <summary>미리보기 목록 생성 (트랜잭션 없음)</summary>
        public static List<RenumberPreview> Preview(List<Element> sorted, RenumberRule rule)
        {
            var list = new List<RenumberPreview>();
            int n = rule.StartNumber;
            foreach (var el in sorted)
            {
                string newNum = BuildNumber(rule.Prefix, n, rule.Digits);
                list.Add(new RenumberPreview
                {
                    Id        = el.Id,
                    OldNumber = GetNumber(el, rule.ParameterName),
                    NewNumber = newNum,
                });
                n += rule.Increment;
            }
            return list;
        }

        /// <summary>실제 번호 설정 (트랜잭션 내부에서 호출)</summary>
        public static int Apply(Document doc, List<RenumberPreview> previews, string paramName)
        {
            int count = 0;
            foreach (var pv in previews)
            {
                var el = doc.GetElement(pv.Id);
                var param = el?.LookupParameter(paramName)
                            ?? el?.get_Parameter(BuiltInParameter.ROOM_NUMBER);
                if (param == null || param.IsReadOnly) continue;
                param.Set(pv.NewNumber);
                count++;
            }
            return count;
        }

        private static string BuildNumber(string prefix, int n, int digits)
            => digits > 0 ? $"{prefix}{n.ToString($"D{digits}")}" : $"{prefix}{n}";

        private static string GetNumber(Element el, string paramName)
        {
            var p = el.LookupParameter(paramName)
                   ?? el.get_Parameter(BuiltInParameter.ROOM_NUMBER);
            return p?.AsString() ?? "";
        }

        private static XYZ GetPoint(Element el)
        {
            if (el.Location is LocationPoint lp) return lp.Point;
            if (el is Room r) return r.Location is LocationPoint rlp ? rlp.Point : XYZ.Zero;
            return XYZ.Zero;
        }

        private static BuiltInCategory? GetBuiltInCategory(string name) => name switch
        {
            "Rooms"  => BuiltInCategory.OST_Rooms,
            "Doors"  => BuiltInCategory.OST_Doors,
            "Spaces" => BuiltInCategory.OST_MEPSpaces,
            _        => null,
        };
    }
}
"""
    filled = await qwen_fill(engine_scaffold,
        "Revit Room, FilteredElementCollector, Parameter.Set(string), BuiltInParameter.ROOM_NUMBER")
    p = out / "ElementRenumberingEngine.cs"
    p.write_text(filled, encoding="utf-8")
    files.append(p)

    command = """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class ElementRenumberingCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var uiDoc = data.Application.ActiveUIDocument;
            var doc   = uiDoc.Document;
            var sel   = uiDoc.Selection.GetElementIds();

            var win = new ElementRenumberingWindow();
            if (win.ShowDialog() != true) return Result.Cancelled;

            var rule    = win.Rule;
            var sorted  = ElementRenumberingEngine.CollectAndSort(doc, sel, rule);
            var preview = ElementRenumberingEngine.Preview(sorted, rule);

            // 미리보기 창
            var previewWin = new RenumberPreviewWindow(preview);
            if (previewWin.ShowDialog() != true) return Result.Cancelled;

            using (var tx = new Transaction(doc, "BCC - Element Renumbering"))
            {
                tx.Start();
                int cnt = ElementRenumberingEngine.Apply(doc, preview, rule.ParameterName);
                tx.Commit();
                TaskDialog.Show("완료", $"{cnt}개 요소 번호 재배정 완료.");
            }
            return Result.Succeeded;
        }
    }
}
"""
    p = out / "ElementRenumberingCommand.cs"
    p.write_text(command, encoding="utf-8")
    files.append(p)

    win_cs = """\
using System.Windows;
using System.Windows.Controls;

namespace BIMCommandCenter.Commands
{
    public partial class ElementRenumberingWindow : Window
    {
        public RenumberRule Rule { get; } = new RenumberRule();
        public ElementRenumberingWindow() => InitializeComponent();

        private void BtnOk_Click(object s, RoutedEventArgs e)
        {
            Rule.CategoryName  = (CboCategory.SelectedItem as ComboBoxItem)?.Content?.ToString() ?? "Rooms";
            Rule.ParameterName = TxtParam.Text.Trim();
            Rule.Prefix        = TxtPrefix.Text;
            Rule.StartNumber   = int.TryParse(TxtStart.Text, out int st) ? st : 1;
            Rule.Increment     = int.TryParse(TxtStep.Text,  out int inc) ? inc : 1;
            Rule.Digits        = int.TryParse(TxtDigits.Text, out int d)  ? d : 0;
            Rule.SortBy        = (SortOrder)(CboSort.SelectedIndex);
            DialogResult = true;
        }
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }

    /// <summary>미리보기 전용 창</summary>
    public partial class RenumberPreviewWindow : Window
    {
        public RenumberPreviewWindow(System.Collections.Generic.List<RenumberPreview> previews)
        {
            InitializeComponent();
            Grid.ItemsSource = previews;
        }
        private void BtnOk_Click(object s, RoutedEventArgs e)     => DialogResult = true;
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }
}
"""
    p = out / "ElementRenumberingWindow.xaml.cs"
    p.write_text(win_cs, encoding="utf-8")
    files.append(p)

    print(f"  [R-04] ElementRenumbering — {len(files)}개 파일 저장")
    return files


# ═════════════════════════════════════════════════════════════════
#  R-05  Project Cleanup Lite
# ═════════════════════════════════════════════════════════════════
async def build_r05() -> list[Path]:
    out = REVIT_ROOT / "ProjectCleanupLite"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    report_cs = """\
using System.Collections.Generic;

namespace BIMCommandCenter.Commands
{
    /// <summary>프로젝트 감사 결과 모델</summary>
    public class CleanupAuditReport
    {
        public int UnplacedViews       { get; set; }
        public int CadImports          { get; set; }
        public int TotalWarnings       { get; set; }
        public int UnplacedRooms       { get; set; }
        public int UnplacedSpaces      { get; set; }
        public int UnusedViewTemplates { get; set; }
        public Dictionary<string, int> WarningByType { get; } = new();
        public List<string>  CadImportNames          { get; } = new();
        public List<string>  UnplacedViewNames        { get; } = new();
    }
}
"""
    p = out / "CleanupAuditReport.cs"
    p.write_text(report_cs, encoding="utf-8")
    files.append(p)

    engine_scaffold = """\
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;

namespace BIMCommandCenter.Commands
{
    /// <summary>프로젝트 정리 감사 엔진 (읽기 전용, 트랜잭션 불필요)</summary>
    public static class ProjectCleanupEngine
    {
        public static CleanupAuditReport RunAudit(Document doc)
        {
            var report = new CleanupAuditReport();

            // 미사용 뷰 (시트에 배치되지 않은 뷰, 뷰 템플릿 제외)
            var allViews = new FilteredElementCollector(doc)
                .OfClass(typeof(View)).Cast<View>()
                .Where(v => !v.IsTemplate && v.CanBePrinted).ToList();
            var placedViewIds = new FilteredElementCollector(doc)
                .OfClass(typeof(Viewport))
                .Cast<Viewport>()
                .Select(vp => vp.ViewId)
                .ToHashSet();
            var unplaced = allViews.Where(v => !placedViewIds.Contains(v.Id)).ToList();
            report.UnplacedViews = unplaced.Count;
            report.UnplacedViewNames.AddRange(unplaced.Take(50).Select(v => v.Name));

            // CAD Import 잔재
            var cads = new FilteredElementCollector(doc)
                .OfClass(typeof(ImportInstance))
                .Cast<ImportInstance>().ToList();
            report.CadImports = cads.Count;
            report.CadImportNames.AddRange(cads.Take(30)
                .Select(c => c.Category?.Name ?? "Unknown"));

            // 경고
            // QWEN_FILL: doc.GetWarnings() 로 FailureMessage 목록 가져와 유형별 집계
            var warnings = doc.GetWarnings();
            report.TotalWarnings = warnings.Count;
            foreach (var w in warnings)
            {
                string key = w.GetDescriptionText();
                if (key.Length > 60) key = key.Substring(0, 60);
                report.WarningByType.TryGetValue(key, out int cnt);
                report.WarningByType[key] = cnt + 1;
            }

            // 미배치 룸
            report.UnplacedRooms = new FilteredElementCollector(doc)
                .OfClass(typeof(SpatialElement))
                .Cast<SpatialElement>()
                .Count(r => r is Room rm && rm.Area < 0.001);

            // 미사용 뷰 템플릿
            var usedTemplateIds = allViews
                .Where(v => v.ViewTemplateId != ElementId.InvalidElementId)
                .Select(v => v.ViewTemplateId).ToHashSet();
            report.UnusedViewTemplates = new FilteredElementCollector(doc)
                .OfClass(typeof(View)).Cast<View>()
                .Count(v => v.IsTemplate && !usedTemplateIds.Contains(v.Id));

            return report;
        }
    }
}
"""
    filled = await qwen_fill(engine_scaffold,
        "doc.GetWarnings() returns IList<FailureMessage>. FailureMessage.GetDescriptionText()")
    p = out / "ProjectCleanupEngine.cs"
    p.write_text(filled, encoding="utf-8")
    files.append(p)

    command = """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.ReadOnly)]
    [Regeneration(RegenerationOption.Manual)]
    public class ProjectCleanupCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc    = data.Application.ActiveUIDocument.Document;
            var report = ProjectCleanupEngine.RunAudit(doc);
            var win    = new ProjectCleanupWindow(report);
            win.ShowDialog();
            return Result.Succeeded;
        }
    }
}
"""
    p = out / "ProjectCleanupCommand.cs"
    p.write_text(command, encoding="utf-8")
    files.append(p)

    print(f"  [R-05] ProjectCleanupLite — {len(files)}개 파일 저장")
    return files


# ═════════════════════════════════════════════════════════════════
#  N-01  Clash Responsibility Board
# ═════════════════════════════════════════════════════════════════
async def build_n01() -> list[Path]:
    out = NAV_ROOT / "ClashResponsibilityBoard" / "src"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    clash_item = """\
namespace NavisworksClashBoard
{
    /// <summary>클래시 결과 데이터 모델</summary>
    public class ClashItem
    {
        public string TestName       { get; set; }
        public string ClashName      { get; set; }
        public string ItemA_Layer    { get; set; }
        public string ItemB_Layer    { get; set; }
        public string DisciplineA    { get; set; }
        public string DisciplineB    { get; set; }
        public string ResponsibleDiscipline { get; set; }
        public string AssigneeName   { get; set; }
        public string AssigneePhone  { get; set; }
        public string Status         { get; set; }
    }
}
"""
    p = out / "ClashItem.cs"
    p.write_text(clash_item, encoding="utf-8")
    files.append(p)

    rule_cs = """\
using System.Collections.Generic;
using Newtonsoft.Json;

namespace NavisworksClashBoard
{
    /// <summary>공종 분류 + 책임자 배정 규칙 (JSON 설정)</summary>
    public class ResponsibilityRule
    {
        [JsonProperty("discipline")]  public string Discipline { get; set; }
        [JsonProperty("keywords")]    public List<string> Keywords { get; set; } = new();
        [JsonProperty("assignee")]    public string Assignee  { get; set; }
        [JsonProperty("phone")]       public string Phone     { get; set; }
    }
}
"""
    p = out / "ResponsibilityRule.cs"
    p.write_text(rule_cs, encoding="utf-8")
    files.append(p)

    grouper_scaffold = """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;
using Newtonsoft.Json;

namespace NavisworksClashBoard
{
    /// <summary>클래시 공종 분류 + 책임자 배정 엔진</summary>
    public static class ClashGrouper
    {
        public static List<ResponsibilityRule> LoadRules(string jsonPath)
            => JsonConvert.DeserializeObject<List<ResponsibilityRule>>(
                   File.ReadAllText(jsonPath)) ?? new List<ResponsibilityRule>();

        public static List<ClashItem> Process(Document doc, List<ResponsibilityRule> rules)
        {
            // QWEN_FILL:
            // 1) doc.GetClash().Tests 로 ClashTest 목록 순회
            // 2) 각 ClashTest.Clashes 로 ClashResult 목록 순회
            // 3) clash.Item1.Path / clash.Item2.Path 에서 레이어/파일명 추출
            // 4) rules 의 keywords 로 공종(DisciplineA/B) 결정
            // 5) 책임 공종 = (A == B) ? A : 두 공종 모두 표시
            // 6) AssigneeName/Phone = 매칭된 rule 에서

            var result = new List<ClashItem>();
            var clashPlugin = ClashPlugin.GetClashPlugin();
            if (clashPlugin == null) return result;

            foreach (ClashTest test in clashPlugin.TestsData.Tests)
            {
                foreach (var clash in test.Clashes)
                {
                    string layerA = GetLayerName(clash.Item1);
                    string layerB = GetLayerName(clash.Item2);
                    string discA  = MatchDiscipline(layerA, rules);
                    string discB  = MatchDiscipline(layerB, rules);
                    var ruleA     = rules.FirstOrDefault(r => r.Discipline == discA);
                    var ruleB     = rules.FirstOrDefault(r => r.Discipline == discB);
                    string responsible = discA == discB ? discA : $"{discA}/{discB}";
                    var assignee = ruleA ?? ruleB;

                    result.Add(new ClashItem
                    {
                        TestName    = test.DisplayName,
                        ClashName   = clash.DisplayName,
                        ItemA_Layer = layerA,
                        ItemB_Layer = layerB,
                        DisciplineA = discA,
                        DisciplineB = discB,
                        ResponsibleDiscipline = responsible,
                        AssigneeName  = assignee?.Assignee ?? "",
                        AssigneePhone = assignee?.Phone    ?? "",
                        Status        = clash.Status.ToString(),
                    });
                }
            }
            return result;
        }

        private static string GetLayerName(ClashElement elem)
        {
            // QWEN_FILL: elem.Model.FileName 또는 elem.Path 에서 파일명/레이어 추출
            try { return System.IO.Path.GetFileNameWithoutExtension(elem.Model.FileName); }
            catch { return "Unknown"; }
        }

        private static string MatchDiscipline(string layer, List<ResponsibilityRule> rules)
        {
            string lower = layer.ToLower();
            foreach (var r in rules)
                if (r.Keywords.Any(k => lower.Contains(k.ToLower())))
                    return r.Discipline;
            return "기타";
        }
    }
}
"""
    filled = await qwen_fill(grouper_scaffold,
        "Navisworks ClashPlugin.GetClashPlugin(), ClashTest.Clashes, ClashResult, ClashElement.Model.FileName")
    p = out / "ClashGrouper.cs"
    p.write_text(filled, encoding="utf-8")
    files.append(p)

    report_gen = """\
using System.Collections.Generic;
using System.IO;
using ClosedXML.Excel;

namespace NavisworksClashBoard
{
    /// <summary>한글 엑셀 리포트 생성기 (ClosedXML)</summary>
    public static class ReportGenerator
    {
        public static string GenerateExcel(List<ClashItem> items, string outputPath)
        {
            using var wb = new XLWorkbook();
            var ws = wb.Worksheets.Add("간섭 책임자 배정");

            // 헤더
            string[] headers = { "번호","클래시명","공종A","공종B","책임공종","담당자","연락처","상태" };
            for (int i = 0; i < headers.Length; i++)
            {
                var cell = ws.Cell(1, i + 1);
                cell.Value = headers[i];
                cell.Style.Font.Bold = true;
                cell.Style.Fill.BackgroundColor = XLColor.SteelBlue;
                cell.Style.Font.FontColor       = XLColor.White;
            }

            // 데이터
            for (int r = 0; r < items.Count; r++)
            {
                var item = items[r];
                ws.Cell(r + 2, 1).Value = r + 1;
                ws.Cell(r + 2, 2).Value = item.ClashName;
                ws.Cell(r + 2, 3).Value = item.DisciplineA;
                ws.Cell(r + 2, 4).Value = item.DisciplineB;
                ws.Cell(r + 2, 5).Value = item.ResponsibleDiscipline;
                ws.Cell(r + 2, 6).Value = item.AssigneeName;
                ws.Cell(r + 2, 7).Value = item.AssigneePhone;
                ws.Cell(r + 2, 8).Value = item.Status;
            }

            ws.Columns().AdjustToContents();
            wb.SaveAs(outputPath);
            return outputPath;
        }
    }
}
"""
    p = out / "ReportGenerator.cs"
    p.write_text(report_gen, encoding="utf-8")
    files.append(p)

    plugin_cs = """\
using System.Windows.Forms;
using System.IO;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Plugins;

namespace NavisworksClashBoard
{
    [Plugin("ClashResponsibilityBoard",
             "LUABIMLABS",
             DisplayName = "간섭 책임자 배정 보드",
             ToolTip     = "Clash Detective 결과를 공종별로 분류하고 책임자를 배정합니다.")]
    [AddInPlugin(AddInLocation.AddIn)]
    public class ClashResponsibilityPlugin : AddInPlugin
    {
        private static readonly string DefaultRulesPath = Path.Combine(
            System.Environment.GetFolderPath(System.Environment.SpecialFolder.MyDocuments),
            "BCC_ClashRules.json");

        public override int Execute(params string[] parameters)
        {
            var doc = Autodesk.Navisworks.Api.Application.ActiveDocument;
            if (doc == null || doc.Models.Count == 0)
            {
                MessageBox.Show("열린 모델이 없습니다.", "오류",
                    MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return 1;
            }

            if (!File.Exists(DefaultRulesPath))
                CreateDefaultRules(DefaultRulesPath);

            var rules = ClashGrouper.LoadRules(DefaultRulesPath);
            var items = ClashGrouper.Process(doc, rules);

            using (var form = new ClashBoardForm(items, DefaultRulesPath))
                form.ShowDialog();

            return 0;
        }

        private static void CreateDefaultRules(string path)
        {
            var defaults = Newtonsoft.Json.JsonConvert.SerializeObject(
                new[]
                {
                    new ResponsibilityRule { Discipline="기계", Keywords=new(){"MEP","MECH","기계","공조"}, Assignee="기계팀장", Phone="010-0000-0001" },
                    new ResponsibilityRule { Discipline="구조", Keywords=new(){"STR","STRUCT","구조"}, Assignee="구조팀장", Phone="010-0000-0002" },
                    new ResponsibilityRule { Discipline="건축", Keywords=new(){"ARC","ARCH","건축"}, Assignee="건축팀장", Phone="010-0000-0003" },
                    new ResponsibilityRule { Discipline="전기", Keywords=new(){"ELE","ELEC","전기"}, Assignee="전기팀장", Phone="010-0000-0004" },
                    new ResponsibilityRule { Discipline="소방", Keywords=new(){"FIRE","소방"}, Assignee="소방팀장", Phone="010-0000-0005" },
                },
                Newtonsoft.Json.Formatting.Indented);
            File.WriteAllText(path, defaults);
        }
    }
}
"""
    p = out / "ClashResponsibilityPlugin.cs"
    p.write_text(plugin_cs, encoding="utf-8")
    files.append(p)

    print(f"  [N-01] ClashResponsibilityBoard — {len(files)}개 파일 저장")
    return files


# ═════════════════════════════════════════════════════════════════
#  N-02  Clash Group Engine
# ═════════════════════════════════════════════════════════════════
async def build_n02() -> list[Path]:
    out = NAV_ROOT / "ClashGroupEngine" / "src"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    rule_cs = """\
using System.Collections.Generic;
using Newtonsoft.Json;

namespace NavisworksClashGroup
{
    public class ClashGroupRule
    {
        [JsonProperty("groupName")] public string GroupName { get; set; }
        [JsonProperty("keywords")]  public List<string> Keywords { get; set; } = new();
        [JsonProperty("statuses")]  public List<string> Statuses { get; set; } = new();
    }
}
"""
    p = out / "ClashGroupRule.cs"
    p.write_text(rule_cs, encoding="utf-8")
    files.append(p)

    engine_scaffold = """\
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Navisworks.Api.Clash;
using Newtonsoft.Json;

namespace NavisworksClashGroup
{
    public static class ClashGroupEngine
    {
        public static List<ClashGroupRule> LoadRules(string path)
            => JsonConvert.DeserializeObject<List<ClashGroupRule>>(File.ReadAllText(path))
               ?? new List<ClashGroupRule>();

        public static void SaveRules(string path, List<ClashGroupRule> rules)
            => File.WriteAllText(path, JsonConvert.SerializeObject(rules, Formatting.Indented));

        /// <summary>ClashTest 내 클래시를 규칙에 따라 그룹 분류</summary>
        public static Dictionary<string, List<ClashResult>> GroupClashes(
            ClashTest test, List<ClashGroupRule> rules)
        {
            // QWEN_FILL: test.Clashes 순회, 각 ClashResult 의
            // DisplayName / Status / Item1.Model.FileName 을 rules[i].Keywords + Statuses 로 매칭
            // 매칭된 그룹에 추가. 매칭 안 되면 "기타" 그룹
            var result = new Dictionary<string, List<ClashResult>>();
            result["기타"] = new List<ClashResult>();
            foreach (var rule in rules) result[rule.GroupName] = new List<ClashResult>();

            foreach (ClashResult clash in test.Clashes)
            {
                string name   = clash.DisplayName?.ToLower() ?? "";
                string status = clash.Status.ToString();
                bool matched  = false;

                foreach (var rule in rules)
                {
                    bool kwMatch     = rule.Keywords.Count == 0
                        || rule.Keywords.Any(k => name.Contains(k.ToLower()));
                    bool statusMatch = rule.Statuses.Count == 0
                        || rule.Statuses.Contains(status);

                    if (kwMatch && statusMatch)
                    {
                        result[rule.GroupName].Add(clash);
                        matched = true;
                        break;
                    }
                }
                if (!matched) result["기타"].Add(clash);
            }
            return result;
        }
    }
}
"""
    filled = await qwen_fill(engine_scaffold,
        "Navisworks ClashTest.Clashes (IEnumerable<ClashResult>), ClashResult.DisplayName, ClashResult.Status")
    p = out / "ClashGroupEngine.cs"
    p.write_text(filled, encoding="utf-8")
    files.append(p)

    plugin_cs = """\
using System.Windows.Forms;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;
using Autodesk.Navisworks.Api.Plugins;

namespace NavisworksClashGroup
{
    [Plugin("ClashGroupEngine",
             "LUABIMLABS",
             DisplayName = "클래시 그룹화",
             ToolTip     = "Clash Detective 결과를 규칙 기반으로 자동 그룹화합니다.")]
    [AddInPlugin(AddInLocation.AddIn)]
    public class ClashGroupPlugin : AddInPlugin
    {
        public override int Execute(params string[] parameters)
        {
            var doc = Autodesk.Navisworks.Api.Application.ActiveDocument;
            if (doc == null)
            { MessageBox.Show("모델을 먼저 여세요."); return 1; }

            using (var form = new ClashGroupForm(doc))
                form.ShowDialog();
            return 0;
        }
    }
}
"""
    p = out / "ClashGroupPlugin.cs"
    p.write_text(plugin_cs, encoding="utf-8")
    files.append(p)

    print(f"  [N-02] ClashGroupEngine — {len(files)}개 파일 저장")
    return files


# ═════════════════════════════════════════════════════════════════
#  N-03  Clash Test Definer
# ═════════════════════════════════════════════════════════════════
async def build_n03() -> list[Path]:
    out = NAV_ROOT / "ClashTestDefiner" / "src"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    def_cs = """\
using Newtonsoft.Json;

namespace NavisworksClashDefiner
{
    public class ClashTestDefinition
    {
        [JsonProperty("testName")]    public string TestName    { get; set; }
        [JsonProperty("selectionA")]  public string SelectionA  { get; set; }
        [JsonProperty("selectionB")]  public string SelectionB  { get; set; }
        [JsonProperty("tolerance")]   public double Tolerance   { get; set; } = 0.025;
        [JsonProperty("type")]        public string ClashType   { get; set; } = "HardClash";
    }
}
"""
    p = out / "ClashTestDefinition.cs"
    p.write_text(def_cs, encoding="utf-8")
    files.append(p)

    engine_scaffold = """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;
using Newtonsoft.Json;

namespace NavisworksClashDefiner
{
    public enum DuplicatePolicy { Skip, Replace }

    public class ClashDefineResult
    {
        public int Created { get; set; }
        public int Skipped { get; set; }
        public List<string> Log { get; } = new List<string>();
    }

    public static class ClashTestDefinerEngine
    {
        public static List<ClashTestDefinition> LoadJson(string path)
            => JsonConvert.DeserializeObject<List<ClashTestDefinition>>(File.ReadAllText(path))
               ?? new List<ClashTestDefinition>();

        public static ClashDefineResult DryRun(
            Document doc, List<ClashTestDefinition> defs, DuplicatePolicy policy)
        {
            // QWEN_FILL: ClashPlugin.GetClashPlugin().TestsData.Tests 로 기존 테스트명 확인
            // defs 각각에 대해 존재 여부 + policy 에 따라 예상 결과 반환
            var result  = new ClashDefineResult();
            var plugin  = ClashPlugin.GetClashPlugin();
            var existing = plugin?.TestsData.Tests.Select(t => t.DisplayName).ToHashSet()
                           ?? new HashSet<string>();
            foreach (var d in defs)
            {
                if (existing.Contains(d.TestName))
                {
                    if (policy == DuplicatePolicy.Skip)
                    { result.Skipped++; result.Log.Add($"SKIP: '{d.TestName}'"); }
                    else
                    { result.Created++; result.Log.Add($"REPLACE: '{d.TestName}'"); }
                }
                else
                { result.Created++; result.Log.Add($"CREATE: '{d.TestName}'"); }
            }
            return result;
        }

        public static ClashDefineResult Execute(
            Document doc, List<ClashTestDefinition> defs, DuplicatePolicy policy)
        {
            // QWEN_FILL:
            // 1) ClashPlugin.GetClashPlugin() 으로 클래시 플러그인 가져오기
            // 2) 각 def 에 대해 TestsData.AddNewTest() 로 ClashTest 생성
            // 3) test.TestType = HardClash/Clearance/Duplicates
            // 4) test.Tolerance = def.Tolerance (미터 단위)
            // 5) SelectionA/B 이름으로 SavedViewpoint 또는 SelectionSet 검색 후 설정
            var result = new ClashDefineResult();
            var plugin = ClashPlugin.GetClashPlugin();
            if (plugin == null) { result.Log.Add("ClashPlugin 로드 실패"); return result; }

            foreach (var def in defs)
            {
                try
                {
                    var existing = plugin.TestsData.Tests
                        .FirstOrDefault(t => t.DisplayName == def.TestName);

                    if (existing != null)
                    {
                        if (policy == DuplicatePolicy.Skip)
                        { result.Skipped++; continue; }
                        plugin.TestsData.Tests.Remove(existing);
                    }

                    var test = plugin.TestsData.Tests.AddNew();
                    test.DisplayName = def.TestName;
                    test.Tolerance   = def.Tolerance;
                    result.Created++;
                    result.Log.Add($"OK: '{def.TestName}'");
                }
                catch (Exception ex)
                { result.Log.Add($"ERR: '{def.TestName}' — {ex.Message}"); }
            }
            return result;
        }
    }
}
"""
    filled = await qwen_fill(engine_scaffold,
        "Navisworks ClashPlugin.GetClashPlugin(), TestsData.Tests.AddNew(), ClashTest.Tolerance, ClashTest.DisplayName")
    p = out / "ClashTestDefinerEngine.cs"
    p.write_text(filled, encoding="utf-8")
    files.append(p)

    plugin_cs = """\
using System.Windows.Forms;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Plugins;

namespace NavisworksClashDefiner
{
    [Plugin("ClashTestDefiner",
             "LUABIMLABS",
             DisplayName = "간섭 테스트 일괄 정의",
             ToolTip     = "JSON 파일로 Clash Detective 테스트를 일괄 생성합니다.")]
    [AddInPlugin(AddInLocation.AddIn)]
    public class ClashTestDefinerPlugin : AddInPlugin
    {
        public override int Execute(params string[] parameters)
        {
            var doc = Autodesk.Navisworks.Api.Application.ActiveDocument;
            if (doc == null)
            { MessageBox.Show("모델을 먼저 여세요."); return 1; }

            using (var form = new ClashTestDefinerForm(doc))
                form.ShowDialog();
            return 0;
        }
    }
}
"""
    p = out / "ClashTestDefinerPlugin.cs"
    p.write_text(plugin_cs, encoding="utf-8")
    files.append(p)

    print(f"  [N-03] ClashTestDefiner — {len(files)}개 파일 저장")
    return files


# ─────────────────────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────────────────────
async def main() -> None:
    print(f"BCC Add-in 스캐폴드 생성 시작 ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print(f"Qwen 모델: {CODER_MODEL} @ {OLLAMA_URL}\n")

    tasks = [
        ("R-01", "Tag/Text Aligner",         "Revit Add-in",      build_r01),
        ("R-02", "View Template Copier",      "Revit Add-in",      build_r02),
        ("R-03", "Type Batch Definer",        "Revit Add-in",      build_r03),
        ("R-04", "Element Renumbering",       "Revit Add-in",      build_r04),
        ("R-05", "Project Cleanup Lite",      "Revit Add-in",      build_r05),
        ("N-01", "Clash Responsibility Board","Navisworks Add-in", build_n01),
        ("N-02", "Clash Group Engine",         "Navisworks Add-in", build_n02),
        ("N-03", "Clash Test Definer",         "Navisworks Add-in", build_n03),
    ]

    for item_id, display, addon_type, builder in tasks:
        print(f"\n{'='*60}\n[{item_id}] {display} ({addon_type})\n{'='*60}")
        files = await builder()
        if files:
            send_email(item_id, display, addon_type, files)
            print(f"  ✓ 이메일 발송 완료")
        else:
            print(f"  ✗ 파일 없음")

    print(f"\n\n전체 완료: {len(tasks)}개 아이템")


if __name__ == "__main__":
    asyncio.run(main())
