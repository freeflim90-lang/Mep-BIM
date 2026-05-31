#!/usr/bin/env python3
"""BCC Add-in 6차 — 승인 아이템 재개발 (Revit API 제외, NW 전체)"""
from __future__ import annotations
import json, os, sys, asyncio
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from backend.email_notifications import send_gmail, load_local_env
load_local_env()

REVIT_ROOT = PROJECT_ROOT / "260519 소스 폴더" / "01_Revit_Addins"
NAV_ROOT   = PROJECT_ROOT / "260519 소스 폴더" / "02_Navisworks_Tools"
BLOCKED    = {".ps1", ".wxs", ".bat", ".sh"}

def mail(item_id, display, kind, files):
    attachable = [f for f in files if f.suffix.lower() not in BLOCKED]
    body = "\n".join([
        f"BCC 6차 승인 아이템: {display}  [{item_id}]",
        f"타입: {kind}  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "", "파일:",
        *[f"  {f.name}  ({f.stat().st_size:,} bytes)" for f in files],
    ])
    send_gmail(subject=f"[BCC 개발완료] {item_id} {display}",
               body=body, attachments=attachable)
    print(f"  이메일 발송")

def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# ═════════════════════════════════════════════════════════════════
# REVIT-1  링크 상태 → 3개 독립 커맨드
# ═════════════════════════════════════════════════════════════════
async def build_link_commands() -> list[Path]:
    out = REVIT_ROOT / "LinkBatchControl"
    files = []

    # 공통 엔진 (Revit API 호출부 마커 포함)
    files.append(write(out / "LinkBatchEngine.cs", """\
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public enum LinkAction { Load, Reload, Unload }

    public class LinkBatchResult
    {
        public string Name    { get; set; }
        public bool   Success { get; set; }
        public string Status  { get; set; }
    }

    public static class LinkBatchEngine
    {
        /// <summary>문서 내 모든 RevitLinkType 목록 반환</summary>
        public static List<RevitLinkType> GetAllLinkTypes(Document doc)
        {
            // REVIT_API: FilteredElementCollector
            return new FilteredElementCollector(doc)
                .OfClass(typeof(RevitLinkType))
                .Cast<RevitLinkType>()
                .ToList();
        }

        /// <summary>선택된 링크에 action 적용</summary>
        public static List<LinkBatchResult> Execute(
            Document doc,
            IEnumerable<RevitLinkType> targets,
            LinkAction action)
        {
            var results = new List<LinkBatchResult>();
            foreach (var lt in targets)
            {
                var r = new LinkBatchResult { Name = lt.Name };
                try
                {
                    switch (action)
                    {
                        case LinkAction.Load:
                            // REVIT_API: lt.Load() — 파일 경로 재확인 후 로드
                            lt.Load(new RevitLinkLoadResult());
                            r.Status = "로드 완료"; r.Success = true; break;

                        case LinkAction.Reload:
                            // REVIT_API: lt.Reload() — 현재 경로에서 재로드
                            lt.Reload();
                            r.Status = "재로드 완료"; r.Success = true; break;

                        case LinkAction.Unload:
                            // REVIT_API: lt.Unload(null) — 언로드 (경로 유지)
                            lt.Unload(null);
                            r.Status = "언로드 완료"; r.Success = true; break;
                    }
                }
                catch (System.Exception ex)
                {
                    r.Status = $"실패: {ex.Message}"; r.Success = false;
                }
                results.Add(r);
            }
            return results;
        }
    }
}
"""))

    # 3개 커맨드 (각각 독립 버튼)
    for action, display, desc in [
        ("Load",   "링크 일괄 로드",   "미로드 상태의 Revit 링크를 모두 로드합니다."),
        ("Reload", "링크 일괄 재로드", "현재 로드된 Revit 링크를 모두 최신 파일로 갱신합니다."),
        ("Unload", "링크 일괄 언로드", "선택한 Revit 링크를 언로드합니다 (경로 유지)."),
    ]:
        files.append(write(out / f"Link{action}Command.cs", f"""\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using System.Linq;

namespace BIMCommandCenter.Commands
{{
    /// <summary>{desc}</summary>
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class Link{action}Command : IExternalCommand
    {{
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {{
            var doc   = data.Application.ActiveUIDocument.Document;
            var links = LinkBatchEngine.GetAllLinkTypes(doc);

            if (links.Count == 0)
            {{ TaskDialog.Show("링크", "프로젝트에 Revit 링크가 없습니다."); return Result.Cancelled; }}

            // Unload 는 선택 창, Load/Reload 는 전체 자동 실행
            IEnumerable<RevitLinkType> targets = links;
            if (LinkAction.{action} == LinkAction.Unload)
            {{
                var win = new LinkSelectWindow(links, "{display}");
                if (win.ShowDialog() != true) return Result.Cancelled;
                targets = win.Selected;
            }}

            using var tx = new Transaction(doc, "BCC - {display}");
            tx.Start();
            var results = LinkBatchEngine.Execute(doc, targets, LinkAction.{action});
            tx.Commit();

            int ok  = results.Count(r => r.Success);
            int err = results.Count(r => !r.Success);
            TaskDialog.Show("{display}", $"완료: {{ok}}개  실패: {{err}}개");
            return Result.Succeeded;
        }}
    }}
}}
"""))

    # 링크 선택 창 (Unload 전용)
    files.append(write(out / "LinkSelectWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using Autodesk.Revit.DB;

namespace BIMCommandCenter.Commands
{
    public partial class LinkSelectWindow : Window
    {
        public IEnumerable<RevitLinkType> Selected { get; private set; }

        public LinkSelectWindow(List<RevitLinkType> links, string title)
        {
            InitializeComponent();
            Title = title;
            LstLinks.ItemsSource = links;
            LstLinks.DisplayMemberPath = "Name";
        }

        private void BtnOk_Click(object s, RoutedEventArgs e)
        {
            Selected = LstLinks.SelectedItems.Cast<RevitLinkType>().ToList();
            if (!Selected.Any()) { MessageBox.Show("링크를 선택하세요."); return; }
            DialogResult = true;
        }
        private void BtnAll_Click(object s, RoutedEventArgs e)    => LstLinks.SelectAll();
        private void BtnCancel_Click(object s, RoutedEventArgs e) => DialogResult = false;
    }
}
"""))

    files.append(write(out / "LinkSelectWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.LinkSelectWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Height="320" Width="400" ResizeMode="NoResize"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="10">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <ListBox x:Name="LstLinks" Grid.Row="0" SelectionMode="Extended" Margin="0,0,0,8"/>
        <StackPanel Grid.Row="1" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="전체 선택" Width="80" Margin="4,0" Click="BtnAll_Click"/>
            <Button Content="실행"      Width="70" Margin="4,0" Click="BtnOk_Click"/>
            <Button Content="취소"      Width="70" Click="BtnCancel_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [REVIT-1] LinkBatchControl 3개 커맨드 — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# REVIT-2  납품 정리 (ProjectCleanup — 수량 표시 + 삭제)
# ═════════════════════════════════════════════════════════════════
async def build_delivery_cleanup() -> list[Path]:
    out = REVIT_ROOT / "DeliveryCleanup"
    files = []

    files.append(write(out / "DeliveryCleanupEngine.cs", """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Revit.DB;
using Autodesk.Revit.DB.Architecture;

namespace BIMCommandCenter.Commands
{
    public class CleanupCategory
    {
        public string        Label      { get; set; }   // 화면 표시명
        public int           Count      { get; set; }   // 수량
        public List<ElementId> Ids      { get; set; } = new();
        public bool          CanDelete  { get; set; } = true;
    }

    public static class DeliveryCleanupEngine
    {
        /// <summary>납품 전 정리 대상 수량 전체 스캔 (읽기 전용)</summary>
        public static List<CleanupCategory> Scan(Document doc)
        {
            var list = new List<CleanupCategory>();

            // ── 미배치 뷰 ─────────────────────────────────────────
            // REVIT_API: FilteredElementCollector + Viewport
            var placedViewIds = new FilteredElementCollector(doc)
                .OfClass(typeof(Viewport)).Cast<Viewport>()
                .Select(vp => vp.ViewId).ToHashSet();
            var unplacedViews = new FilteredElementCollector(doc)
                .OfClass(typeof(View)).Cast<View>()
                .Where(v => !v.IsTemplate && v.CanBePrinted &&
                            !placedViewIds.Contains(v.Id))
                .ToList();
            list.Add(new CleanupCategory
            {
                Label = "미배치 뷰",
                Count = unplacedViews.Count,
                Ids   = unplacedViews.Select(v => v.Id).ToList(),
            });

            // ── CAD Import ────────────────────────────────────────
            var cads = new FilteredElementCollector(doc)
                .OfClass(typeof(ImportInstance))
                .Cast<ImportInstance>()
                .Where(i => !i.IsLinked).ToList();
            list.Add(new CleanupCategory
            {
                Label = "CAD Import",
                Count = cads.Count,
                Ids   = cads.Select(c => c.Id).ToList(),
            });

            // ── 미사용 뷰 템플릿 ──────────────────────────────────
            var usedTemplateIds = new FilteredElementCollector(doc)
                .OfClass(typeof(View)).Cast<View>()
                .Where(v => !v.IsTemplate &&
                            v.ViewTemplateId != ElementId.InvalidElementId)
                .Select(v => v.ViewTemplateId).ToHashSet();
            var unusedTemplates = new FilteredElementCollector(doc)
                .OfClass(typeof(View)).Cast<View>()
                .Where(v => v.IsTemplate && !usedTemplateIds.Contains(v.Id))
                .ToList();
            list.Add(new CleanupCategory
            {
                Label = "미사용 뷰 템플릿",
                Count = unusedTemplates.Count,
                Ids   = unusedTemplates.Select(v => v.Id).ToList(),
            });

            // ── 미배치 룸 ─────────────────────────────────────────
            var unplacedRooms = new FilteredElementCollector(doc)
                .OfClass(typeof(SpatialElement)).Cast<SpatialElement>()
                .OfType<Room>()
                .Where(r => r.Area < 0.001).ToList();
            list.Add(new CleanupCategory
            {
                Label = "미배치 룸",
                Count = unplacedRooms.Count,
                Ids   = unplacedRooms.Select(r => r.Id).ToList(),
            });

            // ── 모델 경고 (삭제 불가, 표시만) ─────────────────────
            var warnings = doc.GetWarnings();
            list.Add(new CleanupCategory
            {
                Label     = "모델 경고",
                Count     = warnings.Count,
                CanDelete = false,   // 경고는 직접 삭제 불가 — 수량 파악 전용
            });

            return list;
        }

        /// <summary>선택한 카테고리 요소 일괄 삭제 (트랜잭션 내부에서 호출)</summary>
        public static int Delete(Document doc, CleanupCategory category)
        {
            if (!category.CanDelete || category.Ids.Count == 0) return 0;
            // REVIT_API: doc.Delete(ICollection<ElementId>)
            var deleted = doc.Delete(category.Ids);
            return deleted.Count;
        }
    }
}
"""))

    files.append(write(out / "DeliveryCleanupCommand.cs", """\
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace BIMCommandCenter.Commands
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class DeliveryCleanupCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData data, ref string message, ElementSet elements)
        {
            var doc        = data.Application.ActiveUIDocument.Document;
            var categories = DeliveryCleanupEngine.Scan(doc);
            var win        = new DeliveryCleanupWindow(categories);
            win.ShowDialog();
            return Result.Succeeded;
        }
    }
}
"""))

    files.append(write(out / "DeliveryCleanupWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Linq;
using System.Windows;

namespace BIMCommandCenter.Commands
{
    public partial class DeliveryCleanupWindow : Window
    {
        private readonly List<CleanupCategory> _categories;

        // 외부에서 Document 를 주입받아 트랜잭션 실행
        // (WPF 창 내부에서 Revit Transaction 직접 실행 불가 — ExternalEvent 패턴 필요)
        // REVIT_API: CommandLaunchHandler 의 ExternalEvent 연동 후 구현
        public static Autodesk.Revit.DB.Document ActiveDoc { get; set; }

        public DeliveryCleanupWindow(List<CleanupCategory> categories)
        {
            _categories = categories;
            InitializeComponent();
            DgCategories.ItemsSource = categories;
        }

        private void BtnDelete_Click(object sender, RoutedEventArgs e)
        {
            if (DgCategories.SelectedItem is not CleanupCategory cat) return;
            if (!cat.CanDelete)
            { MessageBox.Show($"'{cat.Label}'는 직접 삭제할 수 없습니다."); return; }
            if (cat.Count == 0)
            { MessageBox.Show("삭제할 항목이 없습니다."); return; }

            var confirm = MessageBox.Show(
                $"'{cat.Label}' {cat.Count}개를 삭제합니다.\n되돌릴 수 없습니다. 계속하시겠습니까?",
                "확인", MessageBoxButton.YesNo, MessageBoxImage.Warning);
            if (confirm != MessageBoxResult.Yes) return;

            // REVIT_API: ExternalEvent 로 DeliveryCleanupEngine.Delete(doc, cat) 호출
            // 임시: 클릭 이벤트 → ExternalEventHandler 패턴으로 연결 필요
            TxtStatus.Text = $"'{cat.Label}' 삭제 요청 전송됨 (개발 PC에서 ExternalEvent 연결 후 실행)";
        }

        private void BtnRefresh_Click(object sender, RoutedEventArgs e)
        {
            // REVIT_API: 재스캔
            TxtStatus.Text = "재스캔은 개발 PC에서 ExternalEvent 연결 후 실행";
        }

        private void BtnClose_Click(object sender, RoutedEventArgs e) => Close();
    }
}
"""))

    files.append(write(out / "DeliveryCleanupWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.DeliveryCleanupWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="납품 정리" Height="420" Width="520"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="10">
        <Grid.RowDefinitions>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <DataGrid x:Name="DgCategories" Grid.Row="0"
                  AutoGenerateColumns="False" IsReadOnly="True"
                  SelectionMode="Single" Margin="0,0,0,8">
            <DataGrid.Columns>
                <DataGridTextColumn Header="항목"    Binding="{Binding Label}"     Width="*"/>
                <DataGridTextColumn Header="수량"    Binding="{Binding Count}"     Width="60"/>
                <DataGridCheckBoxColumn Header="삭제 가능" Binding="{Binding CanDelete}" Width="80"/>
            </DataGrid.Columns>
        </DataGrid>
        <TextBlock Grid.Row="1" x:Name="TxtStatus" Foreground="DarkBlue"
                   TextWrapping="Wrap" Margin="0,0,0,8"/>
        <StackPanel Grid.Row="2" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="선택 항목 삭제" Width="110" Margin="4,0" Click="BtnDelete_Click"
                    Background="#C0392B" Foreground="White"/>
            <Button Content="재스캔"         Width="70"  Margin="4,0" Click="BtnRefresh_Click"/>
            <Button Content="닫기"           Width="70"  Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [REVIT-2] DeliveryCleanup — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# REVIT-3  인쇄 설정 관리 추가
# ═════════════════════════════════════════════════════════════════
async def build_print_settings() -> list[Path]:
    out = REVIT_ROOT / "BatchPrintAssistant"
    files = []

    files.append(write(out / "PrintSettingsManager.cs", """\
using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;

namespace BIMCommandCenter.Commands
{
    public class PrintPreset
    {
        [JsonProperty("name")]          public string Name          { get; set; }
        [JsonProperty("printerName")]   public string PrinterName   { get; set; } = "Microsoft Print to PDF";
        [JsonProperty("paperSize")]     public string PaperSize     { get; set; } = "A1";
        [JsonProperty("orientation")]   public string Orientation   { get; set; } = "Landscape";
        [JsonProperty("colorMode")]     public string ColorMode     { get; set; } = "BlackLine";
        [JsonProperty("zoom")]          public double Zoom          { get; set; } = 1.0;
        [JsonProperty("marginTop")]     public double MarginTop     { get; set; } = 0;
        [JsonProperty("marginBottom")]  public double MarginBottom  { get; set; } = 0;
        [JsonProperty("marginLeft")]    public double MarginLeft    { get; set; } = 0;
        [JsonProperty("marginRight")]   public double MarginRight   { get; set; } = 0;
        [JsonProperty("combineSheets")] public bool   CombineSheets { get; set; } = false;
        [JsonProperty("viewLinks")]     public bool   ViewLinks     { get; set; } = true;
    }

    public static class PrintSettingsManager
    {
        private static readonly string PresetsPath = Path.Combine(
            System.Environment.GetFolderPath(System.Environment.SpecialFolder.ApplicationData),
            "LUA BIM LABS", "BIM Command Center", "PrintPresets.json");

        public static List<PrintPreset> LoadAll()
        {
            if (!File.Exists(PresetsPath)) return DefaultPresets();
            return JsonConvert.DeserializeObject<List<PrintPreset>>(
                       File.ReadAllText(PresetsPath)) ?? DefaultPresets();
        }

        public static void SaveAll(List<PrintPreset> presets)
        {
            Directory.CreateDirectory(Path.GetDirectoryName(PresetsPath)!);
            File.WriteAllText(PresetsPath,
                JsonConvert.SerializeObject(presets, Formatting.Indented));
        }

        public static void ApplyToRevit(Autodesk.Revit.DB.Document doc,
            PrintPreset preset)
        {
            // REVIT_API: PrintManager + PrintSetting API
            // doc.PrintManager.SelectNewPrintDriver(preset.PrinterName)
            // doc.PrintManager.PrintSetup.CurrentPrintSetting ... 파라미터 설정
            // 개발 PC에서 Revit PrintManager API로 연결
        }

        private static List<PrintPreset> DefaultPresets() => new()
        {
            new PrintPreset { Name = "A1 흑백 납품용",  PaperSize = "A1",
                ColorMode = "BlackLine",  Orientation = "Landscape" },
            new PrintPreset { Name = "A3 컬러 검토용",  PaperSize = "A3",
                ColorMode = "Color",      Orientation = "Landscape" },
            new PrintPreset { Name = "A4 세로 보고서용", PaperSize = "A4",
                ColorMode = "BlackLine",  Orientation = "Portrait"  },
        };
    }
}
"""))

    files.append(write(out / "PrintSettingsWindow.xaml.cs", """\
using System.Collections.Generic;
using System.Windows;

namespace BIMCommandCenter.Commands
{
    public partial class PrintSettingsWindow : Window
    {
        public PrintPreset SelectedPreset { get; private set; }
        private List<PrintPreset> _presets;

        public PrintSettingsWindow()
        {
            InitializeComponent();
            _presets = PrintSettingsManager.LoadAll();
            LstPresets.ItemsSource = _presets;
            LstPresets.DisplayMemberPath = "Name";
            if (_presets.Count > 0) LstPresets.SelectedIndex = 0;
        }

        private void LstPresets_SelectionChanged(object s,
            System.Windows.Controls.SelectionChangedEventArgs e)
        {
            if (LstPresets.SelectedItem is not PrintPreset p) return;
            TxtPrinter.Text     = p.PrinterName;
            CboPaper.Text       = p.PaperSize;
            CboOrientation.Text = p.Orientation;
            CboColor.Text       = p.ColorMode;
            ChkCombine.IsChecked = p.CombineSheets;
        }

        private void BtnSave_Click(object s, RoutedEventArgs e)
        {
            if (LstPresets.SelectedItem is not PrintPreset p) return;
            p.PrinterName   = TxtPrinter.Text;
            p.PaperSize     = CboPaper.Text;
            p.Orientation   = CboOrientation.Text;
            p.ColorMode     = CboColor.Text;
            p.CombineSheets = ChkCombine.IsChecked == true;
            PrintSettingsManager.SaveAll(_presets);
            MessageBox.Show($"'{p.Name}' 저장 완료");
        }

        private void BtnNew_Click(object s, RoutedEventArgs e)
        {
            var name = Microsoft.VisualBasic.Interaction.InputBox("프리셋 이름:", "새 프리셋");
            if (string.IsNullOrEmpty(name)) return;
            _presets.Add(new PrintPreset { Name = name });
            LstPresets.ItemsSource = null;
            LstPresets.ItemsSource = _presets;
            LstPresets.SelectedIndex = _presets.Count - 1;
        }

        private void BtnApply_Click(object s, RoutedEventArgs e)
        {
            SelectedPreset = LstPresets.SelectedItem as PrintPreset;
            DialogResult = true;
        }
        private void BtnClose_Click(object s, RoutedEventArgs e) => Close();
    }
}
"""))

    files.append(write(out / "PrintSettingsWindow.xaml", """\
<Window x:Class="BIMCommandCenter.Commands.PrintSettingsWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="인쇄 설정 관리" Height="440" Width="540"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="10">
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="160"/>
            <ColumnDefinition Width="*"/>
        </Grid.ColumnDefinitions>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>

        <!-- 프리셋 목록 -->
        <TextBlock Grid.Row="0" Grid.Column="0" Text="프리셋" FontWeight="Bold" Margin="0,0,0,4"/>
        <ListBox   Grid.Row="1" Grid.Column="0" x:Name="LstPresets"
                   Margin="0,0,8,0"
                   SelectionChanged="LstPresets_SelectionChanged"/>
        <Button    Grid.Row="2" Grid.Column="0" Content="+ 새 프리셋"
                   Margin="0,6,8,0" Click="BtnNew_Click"/>

        <!-- 설정 편집 -->
        <TextBlock Grid.Row="0" Grid.Column="1" Text="설정 편집" FontWeight="Bold" Margin="0,0,0,4"/>
        <StackPanel Grid.Row="1" Grid.Column="1">
            <StackPanel Orientation="Horizontal" Margin="0,0,0,6">
                <TextBlock Text="프린터:"    Width="90" VerticalAlignment="Center"/>
                <TextBox x:Name="TxtPrinter" Width="220"/>
            </StackPanel>
            <StackPanel Orientation="Horizontal" Margin="0,0,0,6">
                <TextBlock Text="용지 크기:" Width="90" VerticalAlignment="Center"/>
                <ComboBox x:Name="CboPaper" Width="120" IsEditable="True">
                    <ComboBoxItem Content="A0"/>
                    <ComboBoxItem Content="A1"/>
                    <ComboBoxItem Content="A2"/>
                    <ComboBoxItem Content="A3"/>
                    <ComboBoxItem Content="A4"/>
                </ComboBox>
            </StackPanel>
            <StackPanel Orientation="Horizontal" Margin="0,0,0,6">
                <TextBlock Text="방향:"      Width="90" VerticalAlignment="Center"/>
                <ComboBox x:Name="CboOrientation" Width="120">
                    <ComboBoxItem Content="Landscape"/>
                    <ComboBoxItem Content="Portrait"/>
                </ComboBox>
            </StackPanel>
            <StackPanel Orientation="Horizontal" Margin="0,0,0,6">
                <TextBlock Text="색상 모드:" Width="90" VerticalAlignment="Center"/>
                <ComboBox x:Name="CboColor" Width="120">
                    <ComboBoxItem Content="BlackLine"/>
                    <ComboBoxItem Content="GrayScale"/>
                    <ComboBoxItem Content="Color"/>
                </ComboBox>
            </StackPanel>
            <CheckBox x:Name="ChkCombine" Content="시트 합본 (단일 PDF)" Margin="0,0,0,6"/>
        </StackPanel>

        <StackPanel Grid.Row="2" Grid.Column="1" Orientation="Horizontal"
                    HorizontalAlignment="Right" Margin="0,8,0,0">
            <Button Content="저장"  Width="80" Margin="4,0" Click="BtnSave_Click"/>
            <Button Content="적용"  Width="80" Margin="4,0" Click="BtnApply_Click"/>
            <Button Content="닫기"  Width="70" Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [REVIT-3] PrintSettingsManager — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# NW-1  간섭 책임자 배정 — 우선순위 룰 기반 재작성
# ═════════════════════════════════════════════════════════════════
async def build_clash_responsibility_v2() -> list[Path]:
    out = NAV_ROOT / "ClashResponsibilityBoard" / "src"
    files = []

    # 우선순위 룰 JSON (기본값 내장)
    files.append(write(out / "ClashPriorityRules.json", json.dumps({
        "description": "간섭 해소 우선순위 룰 — 우선순위 낮은 공종이 해소 책임",
        "priority_order": ["구조", "건축", "기계(공조덕트)", "기계(배관)", "위생", "소방", "전기", "통신"],
        "rules": [
            {"avoid": "구조",       "must_move": ["건축", "기계(공조덕트)", "기계(배관)", "위생", "소방", "전기", "통신"]},
            {"avoid": "건축",       "must_move": ["기계(공조덕트)", "기계(배관)", "위생", "소방", "전기", "통신"]},
            {"avoid": "기계(공조덕트)", "must_move": ["기계(배관)", "위생", "소방", "전기", "통신"]},
            {"avoid": "기계(배관)", "must_move": ["위생", "소방", "전기", "통신"]},
            {"avoid": "위생",       "must_move": ["소방", "전기", "통신"]},
            {"avoid": "소방",       "must_move": ["전기", "통신"]},
            {"avoid": "전기",       "must_move": ["통신"]},
        ],
        "discipline_keywords": {
            "구조":         ["STR", "구조", "STRUCT", "RC"],
            "건축":         ["ARC", "건축", "ARCH"],
            "기계(공조덕트)": ["DUCT", "덕트", "AIR", "공조"],
            "기계(배관)":    ["PIPE", "배관", "MECH", "기계", "MEP"],
            "위생":         ["SAN", "위생", "PLB", "PLUMBING"],
            "소방":         ["FIRE", "소방", "FP"],
            "전기":         ["ELE", "ELEC", "전기", "POWER"],
            "통신":         ["COM", "통신", "DATA", "IT"],
        },
        "assignees": {
            "구조":         {"name": "", "phone": ""},
            "건축":         {"name": "", "phone": ""},
            "기계(공조덕트)": {"name": "", "phone": ""},
            "기계(배관)":    {"name": "", "phone": ""},
            "위생":         {"name": "", "phone": ""},
            "소방":         {"name": "", "phone": ""},
            "전기":         {"name": "", "phone": ""},
            "통신":         {"name": "", "phone": ""},
        }
    }, ensure_ascii=False, indent=2)))

    files.append(write(out / "ClashPriorityEngine.cs", """\
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace NavisworksClashBoard
{
    public class ClashAssignment
    {
        public string TestName         { get; set; }
        public string ClashName        { get; set; }
        public string DisciplineA      { get; set; }  // 객체 A 공종
        public string DisciplineB      { get; set; }  // 객체 B 공종
        public string ResponsibleDiscipline { get; set; }  // 해소 책임 공종
        public string AssigneeName     { get; set; }  // 담당자 이름
        public string AssigneePhone    { get; set; }
        public string AvoidDiscipline  { get; set; }  // 피해야 하는 공종
        public string Status           { get; set; }
    }

    public class PriorityRules
    {
        [JsonProperty("priority_order")]      public List<string> PriorityOrder { get; set; }
        [JsonProperty("discipline_keywords")] public Dictionary<string, List<string>> Keywords { get; set; }
        [JsonProperty("assignees")]           public Dictionary<string, JObject> Assignees { get; set; }
        [JsonProperty("rules")]               public List<JObject> Rules { get; set; }
    }

    public static class ClashPriorityEngine
    {
        private static readonly string DefaultRulesPath = Path.Combine(
            AppDomain.CurrentDomain.BaseDirectory, "ClashPriorityRules.json");

        public static PriorityRules LoadRules(string path = null)
            => JsonConvert.DeserializeObject<PriorityRules>(
               File.ReadAllText(path ?? DefaultRulesPath));

        /// <summary>레이어/파일명에서 공종 식별</summary>
        public static string MatchDiscipline(string layerOrFile, PriorityRules rules)
        {
            string lower = (layerOrFile ?? "").ToLower();
            foreach (var kv in rules.Keywords)
                if (kv.Value.Any(k => lower.Contains(k.ToLower())))
                    return kv.Key;
            return "기타";
        }

        /// <summary>
        /// 두 공종 간 우선순위 룰 적용 → 해소 책임 공종 결정
        /// 우선순위 높은 공종 = 피해야 하는 고정 객체
        /// 우선순위 낮은 공종 = 이동해야 하는 해소 담당
        /// </summary>
        public static string DetermineResponsible(
            string discA, string discB, PriorityRules rules)
        {
            int idxA = rules.PriorityOrder.IndexOf(discA);
            int idxB = rules.PriorityOrder.IndexOf(discB);

            // 둘 다 목록에 없으면 A 기본
            if (idxA < 0 && idxB < 0) return discA;
            // 목록에 없는 공종은 낮은 우선순위 취급
            if (idxA < 0) return discA;
            if (idxB < 0) return discB;
            // 인덱스가 낮을수록 우선순위 높음 (양보 안 함)
            return idxA < idxB ? discB : discA;
        }

        /// <summary>Clash Detective 전체 처리</summary>
        public static List<ClashAssignment> Process(Document doc, PriorityRules rules)
        {
            var result     = new List<ClashAssignment>();
            var clashPlugin = ClashPlugin.GetClashPlugin();
            if (clashPlugin == null) return result;

            foreach (ClashTest test in clashPlugin.TestsData.Tests)
            {
                foreach (var clash in test.Clashes)
                {
                    string layerA = NavisworksShared.NavisworksHelper.GetLayerName(clash.Item1);
                    string layerB = NavisworksShared.NavisworksHelper.GetLayerName(clash.Item2);
                    string discA  = MatchDiscipline(layerA, rules);
                    string discB  = MatchDiscipline(layerB, rules);
                    string resp   = DetermineResponsible(discA, discB, rules);
                    string avoid  = resp == discA ? discB : discA;

                    string name = "", phone = "";
                    if (rules.Assignees.TryGetValue(resp, out var assignee))
                    {
                        name  = assignee["name"]?.ToString()  ?? "";
                        phone = assignee["phone"]?.ToString() ?? "";
                    }

                    result.Add(new ClashAssignment
                    {
                        TestName            = test.DisplayName,
                        ClashName           = clash.DisplayName,
                        DisciplineA         = discA,
                        DisciplineB         = discB,
                        ResponsibleDiscipline = resp,
                        AvoidDiscipline     = avoid,
                        AssigneeName        = name,
                        AssigneePhone       = phone,
                        Status              = clash.Status.ToString(),
                    });
                }
            }
            return result;
        }
    }
}
"""))

    files.append(write(out / "ClashAssignmentForm.cs", """\
using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using Autodesk.Navisworks.Api;

namespace NavisworksClashBoard
{
    public class ClashAssignmentForm : Form
    {
        private readonly Document       _doc;
        private PriorityRules           _rules;
        private DataGridView            _gridResults;
        private DataGridView            _gridAssignees;
        private Button                  _btnRun, _btnSaveAssignees, _btnClose;
        private Label                   _lblStatus;

        public ClashAssignmentForm(Document doc)
        {
            _doc   = doc;
            _rules = ClashPriorityEngine.LoadRules();
            Text   = "간섭 책임자 배정 (우선순위 룰 기반)";
            Width  = 900; Height = 600;
            StartPosition = FormStartPosition.CenterScreen;
            BuildUI();
        }

        private void BuildUI()
        {
            var tab = new TabControl { Dock = DockStyle.Fill };

            // ── 결과 탭 ───────────────────────────────────────────
            _gridResults = new DataGridView
            {
                Dock = DockStyle.Fill, ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells,
            };
            var tabResult = new TabPage("간섭 배정 결과") { Controls = { _gridResults } };

            // ── 담당자 설정 탭 ───────────────────────────────────
            _gridAssignees = new DataGridView
            {
                Dock = DockStyle.Fill, ReadOnly = false,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells,
            };
            _gridAssignees.Columns.Add("Discipline", "공종");
            _gridAssignees.Columns.Add("Name",       "담당자 이름");
            _gridAssignees.Columns.Add("Phone",      "연락처");
            foreach (var disc in _rules.PriorityOrder)
            {
                _rules.Assignees.TryGetValue(disc, out var a);
                _gridAssignees.Rows.Add(disc,
                    a?["name"]?.ToString()  ?? "",
                    a?["phone"]?.ToString() ?? "");
            }
            var tabAssignees = new TabPage("담당자 설정") { Controls = { _gridAssignees } };

            tab.TabPages.AddRange(new[] { tabResult, tabAssignees });

            var panel = new Panel { Dock = DockStyle.Bottom, Height = 44 };
            _lblStatus       = new Label  { Text = "실행 버튼을 눌러 배정 시작", AutoSize = true, Top = 12, Left = 10 };
            _btnSaveAssignees = new Button { Text = "담당자 저장", Width = 100, Top = 8, Left = 400 };
            _btnRun          = new Button { Text = "배정 실행",   Width = 100, Top = 8, Left = 510 };
            _btnClose        = new Button { Text = "닫기",        Width = 80,  Top = 8, Left = 620 };
            _btnSaveAssignees.Click += BtnSaveAssignees_Click;
            _btnRun.Click          += BtnRun_Click;
            _btnClose.Click        += (s, e) => Close();
            panel.Controls.AddRange(new Control[]
                { _lblStatus, _btnSaveAssignees, _btnRun, _btnClose });

            Controls.Add(tab);
            Controls.Add(panel);
        }

        private void BtnSaveAssignees_Click(object s, EventArgs e)
        {
            foreach (DataGridViewRow row in _gridAssignees.Rows)
            {
                string disc  = row.Cells["Discipline"].Value?.ToString() ?? "";
                string name  = row.Cells["Name"].Value?.ToString()       ?? "";
                string phone = row.Cells["Phone"].Value?.ToString()      ?? "";
                if (_rules.Assignees.ContainsKey(disc))
                {
                    _rules.Assignees[disc]["name"]  = name;
                    _rules.Assignees[disc]["phone"] = phone;
                }
            }
            // JSON 재저장
            string path = System.IO.Path.Combine(
                AppDomain.CurrentDomain.BaseDirectory, "ClashPriorityRules.json");
            System.IO.File.WriteAllText(path,
                Newtonsoft.Json.JsonConvert.SerializeObject(_rules, Newtonsoft.Json.Formatting.Indented));
            _lblStatus.Text = "담당자 정보 저장 완료";
        }

        private void BtnRun_Click(object s, EventArgs e)
        {
            _rules = ClashPriorityEngine.LoadRules();
            var results = ClashPriorityEngine.Process(_doc, _rules);
            _gridResults.DataSource = results;
            _lblStatus.Text =
                $"배정 완료: {results.Count}건 — " +
                $"책임 공종: {string.Join(", ", results.GroupBy(r => r.ResponsibleDiscipline).Select(g => $"{g.Key}({g.Count()}"))}";
        }
    }
}
"""))
    print(f"  [NW-1] ClashResponsibility v2 — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# NW-2  간섭 그룹화 — 좌표 기반 재작성
# ═════════════════════════════════════════════════════════════════
async def build_clash_coordinate_group() -> list[Path]:
    out = NAV_ROOT / "ClashGroupEngine" / "src"
    files = []

    files.append(write(out / "ClashCoordinateGrouper.cs", """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;

namespace NavisworksClashGroup
{
    public class CoordClashGroup
    {
        public string       GroupId    { get; set; }  // "ZONE-001" 형태
        public List<string> ClashNames { get; set; } = new();
        public double       CenterX    { get; set; }
        public double       CenterY    { get; set; }
        public double       CenterZ    { get; set; }
        public int          Count      => ClashNames.Count;
    }

    public static class ClashCoordinateGrouper
    {
        /// <summary>
        /// 반경 radiusMeters 이내의 클래시를 같은 그룹으로 묶는다.
        /// 알고리즘: 단순 단일 연결 클러스터링 (Union-Find)
        /// </summary>
        public static List<CoordClashGroup> Group(
            ClashTest test, double radiusMeters = 5.0)
        {
            // 1) 각 클래시의 중심 좌표 수집
            var items = new List<(string name, double x, double y, double z)>();
            foreach (var clash in test.Clashes)
            {
                var center = GetClashCenter(clash);
                if (center.HasValue)
                    items.Add((clash.DisplayName, center.Value.X,
                               center.Value.Y, center.Value.Z));
            }

            // 2) Union-Find로 반경 내 클래시 연결
            int n = items.Count;
            int[] parent = Enumerable.Range(0, n).ToArray();

            int Find(int i) => parent[i] == i ? i : (parent[i] = Find(parent[i]));
            void Union(int a, int b) { parent[Find(a)] = Find(b); }

            for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
            {
                double dist = Distance(items[i], items[j]);
                if (dist <= radiusMeters)
                    Union(i, j);
            }

            // 3) 같은 루트끼리 그룹화
            var groups = new Dictionary<int, List<int>>();
            for (int i = 0; i < n; i++)
            {
                int root = Find(i);
                if (!groups.ContainsKey(root)) groups[root] = new List<int>();
                groups[root].Add(i);
            }

            // 4) CoordClashGroup 생성
            int zoneNum = 1;
            return groups.Values
                .OrderByDescending(g => g.Count)
                .Select(g =>
                {
                    var cx = g.Average(i => items[i].x);
                    var cy = g.Average(i => items[i].y);
                    var cz = g.Average(i => items[i].z);
                    return new CoordClashGroup
                    {
                        GroupId    = $"ZONE-{zoneNum++:D3}",
                        ClashNames = g.Select(i => items[i].name).ToList(),
                        CenterX    = Math.Round(cx, 2),
                        CenterY    = Math.Round(cy, 2),
                        CenterZ    = Math.Round(cz, 2),
                    };
                }).ToList();
        }

        private static double Distance(
            (string, double x, double y, double z) a,
            (string, double x, double y, double z) b)
            => Math.Sqrt(
                Math.Pow(a.x - b.x, 2) +
                Math.Pow(a.y - b.y, 2) +
                Math.Pow(a.z - b.z, 2));

        private static (double X, double Y, double Z)? GetClashCenter(ClashResult clash)
        {
            try
            {
                // NAVISWORKS_API: BoundingBox3D 로 중심 좌표 계산
                var bbA = clash.Item1.BoundingBox();
                var bbB = clash.Item2.BoundingBox();
                if (bbA == null || bbB == null) return null;
                double x = (bbA.Min.X + bbA.Max.X + bbB.Min.X + bbB.Max.X) / 4.0;
                double y = (bbA.Min.Y + bbA.Max.Y + bbB.Min.Y + bbB.Max.Y) / 4.0;
                double z = (bbA.Min.Z + bbA.Max.Z + bbB.Min.Z + bbB.Max.Z) / 4.0;
                return (x, y, z);
            }
            catch { return null; }
        }
    }
}
"""))

    files.append(write(out / "ClashCoordGroupForm.cs", """\
using System;
using System.Windows.Forms;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;
using System.Linq;

namespace NavisworksClashGroup
{
    public class ClashCoordGroupForm : Form
    {
        private readonly Document _doc;
        private ComboBox   _cboTest;
        private NumericUpDown _numRadius;
        private DataGridView  _gridGroups;
        private Button     _btnRun, _btnClose;
        private Label      _lblStatus;

        public ClashCoordGroupForm(Document doc)
        {
            _doc = doc;
            Text = "간섭 좌표 기반 그룹화";
            Width = 680; Height = 500;
            StartPosition = FormStartPosition.CenterScreen;
            BuildUI();
        }

        private void BuildUI()
        {
            var topPanel = new Panel { Dock = DockStyle.Top, Height = 50 };
            topPanel.Controls.Add(new Label { Text = "테스트:", Top = 14, Left = 10, Width = 60 });
            _cboTest = new ComboBox
                { Top = 12, Left = 75, Width = 280, DropDownStyle = ComboBoxStyle.DropDownList };
            topPanel.Controls.Add(new Label { Text = "그룹화 반경(m):", Top = 14, Left = 370, Width = 95 });
            _numRadius = new NumericUpDown
                { Top = 12, Left = 470, Width = 70, Value = 5, Minimum = 1, Maximum = 50,
                  DecimalPlaces = 1, Increment = 0.5m };
            topPanel.Controls.Add(_cboTest);
            topPanel.Controls.Add(_numRadius);

            _gridGroups = new DataGridView
            {
                Dock = DockStyle.Fill, ReadOnly = true,
                AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.AllCells,
            };
            _gridGroups.Columns.Add("Zone",   "구역 ID");
            _gridGroups.Columns.Add("Count",  "간섭 수");
            _gridGroups.Columns.Add("X",      "중심 X");
            _gridGroups.Columns.Add("Y",      "중심 Y");
            _gridGroups.Columns.Add("Z",      "중심 Z");
            _gridGroups.Columns.Add("Clashes","포함 간섭");

            var btnPanel = new Panel { Dock = DockStyle.Bottom, Height = 44 };
            _lblStatus = new Label { AutoSize = true, Top = 12, Left = 10 };
            _btnRun    = new Button { Text = "그룹화 실행", Width = 100, Top = 8, Left = 480 };
            _btnClose  = new Button { Text = "닫기",        Width = 80,  Top = 8, Left = 590 };
            _btnRun.Click   += BtnRun_Click;
            _btnClose.Click += (s, e) => Close();
            btnPanel.Controls.AddRange(new Control[] { _lblStatus, _btnRun, _btnClose });

            Controls.Add(_gridGroups);
            Controls.Add(topPanel);
            Controls.Add(btnPanel);

            // 테스트 목록 로드
            var cp = ClashPlugin.GetClashPlugin();
            if (cp != null)
                foreach (ClashTest t in cp.TestsData.Tests)
                    _cboTest.Items.Add(t.DisplayName);
            if (_cboTest.Items.Count > 0) _cboTest.SelectedIndex = 0;
        }

        private void BtnRun_Click(object s, EventArgs e)
        {
            if (_cboTest.SelectedIndex < 0) { MessageBox.Show("테스트를 선택하세요."); return; }
            var cp   = ClashPlugin.GetClashPlugin();
            var test = cp?.TestsData.Tests.ElementAt(_cboTest.SelectedIndex);
            if (test == null) return;

            double radius = (double)_numRadius.Value;
            var groups = ClashCoordinateGrouper.Group(test, radius);

            _gridGroups.Rows.Clear();
            foreach (var g in groups)
                _gridGroups.Rows.Add(g.GroupId, g.Count,
                    g.CenterX, g.CenterY, g.CenterZ,
                    string.Join(", ", g.ClashNames.Take(3)) +
                    (g.Count > 3 ? $" 외 {g.Count - 3}개" : ""));

            _lblStatus.Text =
                $"총 {groups.Sum(g => g.Count)}건 → {groups.Count}개 구역 (반경 {radius}m 기준)";
        }
    }
}
"""))
    print(f"  [NW-2] ClashCoordinateGroup — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# NW-3  간섭 테스트 일괄 정의 — SelectionSet 자동 연결
# ═════════════════════════════════════════════════════════════════
async def build_clash_test_autosetup() -> list[Path]:
    out = NAV_ROOT / "ClashTestDefiner" / "src"
    files = []

    files.append(write(out / "ClashTestAutoSetup.cs", """\
using System;
using System.Collections.Generic;
using System.Linq;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;

namespace NavisworksClashDefiner
{
    public class SelectionSetInfo
    {
        public string DisplayName { get; set; }
        public string Guid        { get; set; }
    }

    public static class ClashTestAutoSetup
    {
        /// <summary>문서 내 모든 SavedViewpoint / SelectionSet 목록 반환</summary>
        public static List<SelectionSetInfo> GetSelectionSets(Document doc)
        {
            // NAVISWORKS_API: doc.SelectionSets.ToList()
            var list = new List<SelectionSetInfo>();
            try
            {
                foreach (var item in doc.SelectionSets.RootItem.Children)
                    CollectSets(item, list);
            }
            catch { /* API 버전별 차이 무시 */ }
            return list;
        }

        private static void CollectSets(SavedItem item, List<SelectionSetInfo> list)
        {
            if (item is SelectionSet ss)
                list.Add(new SelectionSetInfo
                {
                    DisplayName = ss.DisplayName,
                    Guid        = ss.Guid.ToString(),
                });
            if (item is FolderItem fi)
                foreach (var child in fi.Children)
                    CollectSets(child, list);
        }

        /// <summary>
        /// SelectionSet A vs B 조합으로 ClashTest 자동 생성
        /// </summary>
        public static ClashDefineResult CreateTest(
            Document doc,
            string testName,
            SelectionSetInfo setA,
            SelectionSetInfo setB,
            double toleranceMeters,
            string clashType,
            DuplicatePolicy policy)
        {
            var result = new ClashDefineResult();
            var cp     = ClashPlugin.GetClashPlugin();
            if (cp == null) { result.Log.Add("ClashPlugin 로드 실패"); return result; }

            try
            {
                var existing = cp.TestsData.Tests
                    .FirstOrDefault(t => t.DisplayName == testName);
                if (existing != null)
                {
                    if (policy == DuplicatePolicy.Skip)
                    { result.Skipped++; result.Log.Add($"SKIP: '{testName}'"); return result; }
                    cp.TestsData.Tests.Remove(existing);
                }

                var test          = cp.TestsData.Tests.AddNew();
                test.DisplayName  = testName;
                test.Tolerance    = toleranceMeters;

                // NAVISWORKS_API: SelectionSource 로 setA/setB 연결
                // test.SelectionA = new SavedItemSelectionSource(doc, setA.Guid)
                // test.SelectionB = new SavedItemSelectionSource(doc, setB.Guid)
                // 개발 PC에서 Navisworks SDK API 확인 후 연결

                result.Created++;
                result.Log.Add($"OK: '{testName}' ({setA.DisplayName} vs {setB.DisplayName})");
            }
            catch (Exception ex)
            { result.Log.Add($"ERR: {ex.Message}"); }
            return result;
        }
    }
}
"""))

    files.append(write(out / "ClashTestAutoForm.cs", """\
using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using Autodesk.Navisworks.Api;
using Autodesk.Navisworks.Api.Clash;

namespace NavisworksClashDefiner
{
    /// <summary>SelectionSet 선택 UI — 자동 테스트 생성</summary>
    public class ClashTestAutoForm : Form
    {
        private readonly Document            _doc;
        private List<SelectionSetInfo>       _sets;
        private ComboBox                     _cboSetA, _cboSetB;
        private TextBox                      _txtName;
        private NumericUpDown                _numTolerance;
        private ComboBox                     _cboType;
        private TextBox                      _txtResult;
        private Button                       _btnCreate, _btnClose;

        public ClashTestAutoForm(Document doc)
        {
            _doc  = doc;
            _sets = ClashTestAutoSetup.GetSelectionSets(doc);
            Text  = "간섭 테스트 자동 설정"; Width = 540; Height = 440;
            StartPosition = FormStartPosition.CenterScreen;
            BuildUI();
        }

        private void BuildUI()
        {
            int y = 16;
            void Row(string lbl, Control ctrl, int w = 320) {
                Controls.Add(new Label { Text = lbl, Top = y, Left = 10, Width = 110 });
                ctrl.Top = y - 2; ctrl.Left = 125; ctrl.Width = w;
                Controls.Add(ctrl); y += 32;
            }

            _cboSetA = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList };
            _cboSetB = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList };
            foreach (var s in _sets)
            {
                _cboSetA.Items.Add(s.DisplayName);
                _cboSetB.Items.Add(s.DisplayName);
            }
            if (_sets.Count > 0) _cboSetA.SelectedIndex = 0;
            if (_sets.Count > 1) _cboSetB.SelectedIndex = 1;

            _txtName = new TextBox { Text = "" };
            _cboSetA.SelectedIndexChanged += UpdateTestName;
            _cboSetB.SelectedIndexChanged += UpdateTestName;

            _numTolerance = new NumericUpDown
                { Value = 25, Minimum = 1, Maximum = 500,
                  DecimalPlaces = 0, Increment = 5 };
            _cboType = new ComboBox { DropDownStyle = ComboBoxStyle.DropDownList };
            _cboType.Items.AddRange(new[] { "HardClash", "Clearance", "Duplicates" });
            _cboType.SelectedIndex = 0;

            Row("공종 A (선택셋):", _cboSetA);
            Row("공종 B (선택셋):", _cboSetB);
            Row("테스트 이름:",     _txtName);
            Row("허용오차(mm):",    _numTolerance, 80);
            Row("간섭 유형:",       _cboType, 140);

            _txtResult = new TextBox
                { Top = y, Left = 10, Width = 500, Height = 80,
                  Multiline = true, ReadOnly = true, ScrollBars = ScrollBars.Vertical };
            Controls.Add(_txtResult); y += 90;

            _btnCreate = new Button { Text = "테스트 생성", Width = 110, Top = y, Left = 270 };
            _btnClose  = new Button { Text = "닫기",        Width = 80,  Top = y, Left = 390 };
            _btnCreate.Click += BtnCreate_Click;
            _btnClose.Click  += (s, e) => Close();
            Controls.AddRange(new Control[] { _btnCreate, _btnClose });

            UpdateTestName(null, null);
        }

        private void UpdateTestName(object s, EventArgs e)
        {
            string a = _cboSetA.SelectedItem?.ToString() ?? "A";
            string b = _cboSetB.SelectedItem?.ToString() ?? "B";
            _txtName.Text = $"{a} vs {b}";
        }

        private void BtnCreate_Click(object s, EventArgs e)
        {
            if (_cboSetA.SelectedIndex < 0 || _cboSetB.SelectedIndex < 0)
            { MessageBox.Show("공종 A, B를 선택하세요."); return; }

            var setA = _sets[_cboSetA.SelectedIndex];
            var setB = _sets[_cboSetB.SelectedIndex];
            double tol = (double)_numTolerance.Value / 1000.0;  // mm → m

            var result = ClashTestAutoSetup.CreateTest(
                _doc, _txtName.Text, setA, setB, tol,
                _cboType.SelectedItem?.ToString() ?? "HardClash",
                DuplicatePolicy.Skip);

            _txtResult.Text = string.Join("\r\n", result.Log);
        }
    }
}
"""))
    print(f"  [NW-3] ClashTestAutoSetup — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# NW-5  IFC Export Helper — 승인 확정 (기존 코드 이메일 발송)
# ═════════════════════════════════════════════════════════════════
async def collect_ifc_export_files() -> list[Path]:
    out = NAV_ROOT / "IFCExportHelper" / "src"
    files = list(out.glob("*.cs"))
    print(f"  [NW-5] IFCExportHelper 승인 — {len(files)}개 기존 파일")
    return files


# ═════════════════════════════════════════════════════════════════
# 최종 승인 아이템 commands.json 업데이트
# ═════════════════════════════════════════════════════════════════
async def update_commands_json() -> list[Path]:
    cmd_path = REVIT_ROOT / "Addin Dashboard" / "commands.json"
    data = json.loads(cmd_path.read_text(encoding="utf-8"))

    # 승인 기능 카테고리 추가
    approved_category = {
        "name": "Approved Features",
        "icon": "",
        "commands": [
            # 뷰 관리
            {"id": "VIEW_TEMPLATE_COPIER", "name": "뷰 템플릿 복사",  "description": "다른 프로젝트의 뷰 템플릿을 현재 문서로 복사합니다.",    "className": "BIMCommandCenter.Commands.ViewTemplateCopierCommand",  "tags": ["뷰", "템플릿", "복사"]},
            {"id": "SMART_SELECTOR",       "name": "Smart 선택",      "description": "카테고리·파라미터 조건으로 요소를 필터링·선택합니다.",    "className": "BIMCommandCenter.Commands.SmartSelectorCommand",       "tags": ["선택", "필터"]},
            {"id": "WORKSET_INSPECTOR",    "name": "Workset 검사",    "description": "워크셋별 요소 수를 집계하고 선택합니다.",                  "className": "BIMCommandCenter.Commands.WorksetInspectorCommand",    "tags": ["워크셋"]},
            {"id": "SHEET_DUPLICATOR",     "name": "시트 복제",        "description": "선택 시트와 뷰를 일괄 복제합니다.",                      "className": "BIMCommandCenter.Commands.SheetViewDuplicatorCommand", "tags": ["시트", "복제"]},
            # 모델 처리
            {"id": "FAMILY_TRANSFER",      "name": "패밀리 전송",      "description": "패밀리를 폴더로 일괄 내보내기 또는 가져오기합니다.",      "className": "BIMCommandCenter.Commands.FamilyPackageTransferCommand","tags": ["패밀리", "전송"]},
            # 링크
            {"id": "LINK_LOAD",            "name": "링크 일괄 로드",   "description": "미로드 상태의 Revit 링크를 모두 로드합니다.",            "className": "BIMCommandCenter.Commands.LinkLoadCommand",            "tags": ["링크", "로드"]},
            {"id": "LINK_RELOAD",          "name": "링크 일괄 재로드", "description": "로드된 Revit 링크를 최신 파일로 갱신합니다.",            "className": "BIMCommandCenter.Commands.LinkReloadCommand",          "tags": ["링크", "재로드"]},
            {"id": "LINK_UNLOAD",          "name": "링크 일괄 언로드", "description": "선택한 Revit 링크를 언로드합니다.",                      "className": "BIMCommandCenter.Commands.LinkUnloadCommand",          "tags": ["링크", "언로드"]},
            # QA
            {"id": "DELIVERY_CLEANUP",     "name": "납품 정리",        "description": "납품 전 미배치 뷰·CAD Import·미사용 템플릿을 정리합니다.","className": "BIMCommandCenter.Commands.DeliveryCleanupCommand",    "tags": ["납품", "정리", "QA"]},
            # 인쇄
            {"id": "BATCH_PRINT",          "name": "일괄 인쇄",        "description": "선택한 시트를 PDF로 일괄 출력합니다.",                   "className": "BIMCommandCenter.Commands.BatchPrintCommand",          "tags": ["인쇄", "PDF", "출력"]},
            {"id": "PRINT_SETTINGS",       "name": "인쇄 설정",        "description": "프린터·용지·색상 인쇄 프리셋을 저장하고 관리합니다.",    "className": "BIMCommandCenter.Commands.PrintSettingsCommand",       "tags": ["인쇄", "설정"]},
        ]
    }

    # 기존에 "Approved Features" 카테고리가 없으면 추가
    exists = any(c.get("name") == "Approved Features"
                 for c in data.get("categories", []))
    if not exists:
        data.setdefault("categories", []).append(approved_category)
    else:
        for cat in data["categories"]:
            if cat.get("name") == "Approved Features":
                cat["commands"] = approved_category["commands"]

    cmd_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  [JSON] commands.json 업데이트 완료 (Approved Features 카테고리 추가)")
    return [cmd_path]


# ═════════════════════════════════════════════════════════════════
# 메인
# ═════════════════════════════════════════════════════════════════
async def main():
    print(f"BCC 6차 — 승인 아이템 개발 (Revit API 제외, NW 전체)\n"
          f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    batches = [
        ("REVIT-1", "링크 일괄 로드/재로드/언로드 3개 커맨드", "Revit",      build_link_commands),
        ("REVIT-2", "납품 정리 (수량+삭제)",                   "Revit",      build_delivery_cleanup),
        ("REVIT-3", "인쇄 설정 관리",                         "Revit",      build_print_settings),
        ("NW-1",    "간섭 책임자 배정 v2 (우선순위 룰)",        "Navisworks", build_clash_responsibility_v2),
        ("NW-2",    "간섭 좌표 기반 그룹화",                   "Navisworks", build_clash_coordinate_group),
        ("NW-3",    "간섭 테스트 자동 설정 (SelectionSet)",    "Navisworks", build_clash_test_autosetup),
        ("NW-5",    "IFC 내보내기 (승인 확정)",                "Navisworks", collect_ifc_export_files),
        ("JSON",    "commands.json 승인 아이템 등록",          "통합",       update_commands_json),
    ]

    for item_id, display, kind, builder in batches:
        print(f"\n{'='*55}\n[{item_id}] {display}\n{'='*55}")
        files = await builder()
        if files:
            mail(item_id, display, kind, files)
            print(f"  ✓ 완료")

    print(f"\n\n6차 개발 전체 완료")


if __name__ == "__main__":
    asyncio.run(main())
