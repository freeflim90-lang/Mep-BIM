#!/usr/bin/env python3
"""BCC Add-in 5차 개발 러너 — 인프라·빌드·라이선스·NW 프로젝트"""
from __future__ import annotations
import json, os, sys, asyncio
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from backend.email_notifications import send_gmail, load_local_env
load_local_env()

REVIT_ROOT  = PROJECT_ROOT / "260519 소스 폴더" / "01_Revit_Addins"
NAV_ROOT    = PROJECT_ROOT / "260519 소스 폴더" / "02_Navisworks_Tools"
ADDIN_DASH  = REVIT_ROOT / "Addin Dashboard"


BLOCKED_EXTS = {".ps1", ".wxs", ".bat", ".sh", ".vbs", ".cmd", ".js"}

def mail(item_id: str, display: str, kind: str, files: list[Path]) -> None:
    attachable = [f for f in files if f.suffix.lower() not in BLOCKED_EXTS]
    blocked    = [f for f in files if f.suffix.lower() in BLOCKED_EXTS]
    body_lines = [
        f"BCC 5차: {display}  [{item_id}]",
        f"타입: {kind}  |  완료: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]
    if attachable:
        body_lines += ["첨부 파일:", *[f"  {f.name} ({f.stat().st_size:,} bytes)" for f in attachable]]
    if blocked:
        body_lines += ["", "로컬 생성 파일 (Gmail 보안 제한으로 첨부 제외):",
                       *[f"  {f}" for f in blocked]]
    send_gmail(
        subject=f"[BCC 개발완료] {item_id} {display}",
        body="\n".join(body_lines),
        attachments=attachable,
    )
    print(f"  이메일 발송")


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


# ═════════════════════════════════════════════════════════════════
# 1  BIMCommandCenter.csproj 업데이트
# ═════════════════════════════════════════════════════════════════
async def update_csproj() -> list[Path]:
    csproj = ADDIN_DASH / "BIMCommandCenter.csproj"
    content = csproj.read_text(encoding="utf-8")

    # ClosedXML 이미 있으면 스킵
    if "ClosedXML" in content:
        print("  .csproj: ClosedXML 이미 포함 — 신규 파일 ItemGroup만 추가")

    # 새 폴더 목록 (Addin Dashboard 밖에 있는 신규 폴더들)
    new_folders = [
        "TagTextAligner", "ViewTemplateCopier", "TypeBatchDefiner",
        "ElementRenumbering", "ProjectCleanupLite",
        "LineCleanupLite", "SmartSelectorLite", "WorksetInspectorLite",
        "LinkHealthReload", "ScheduleExcelExport", "ScheduleExcelSync",
        "MEPLengthCalculator", "WarningManager",
        "BatchPrintAssistant", "SheetViewDuplicator", "RoomFinishingPro",
        "IFCDeliveryValidator", "MultiMaterialTagger", "FamilyPackageTransfer",
    ]

    rel_cs_items   = "\n".join(
        f'    <Compile Include="..\\{f}\\*.cs" />' for f in new_folders)
    rel_xaml_items = "\n".join(
        f'    <Page Include="..\\{f}\\*.xaml">\n      <Generator>MSBuild:Compile</Generator>\n    </Page>'
        for f in new_folders)
    rel_cfg_items  = "\n".join(
        f'    <None Update="..\\{f}\\Configs\\*.json">\n      <CopyToOutputDirectory>Always</CopyToOutputDirectory>\n    </None>'
        for f in ["IFCDeliveryValidator"])

    additions = f"""
  <!-- ── 4차까지 추가된 신규 커맨드 소스 파일 ────────────────── -->
  <ItemGroup>
{rel_cs_items}
  </ItemGroup>

  <ItemGroup>
{rel_xaml_items}
  </ItemGroup>

  <!-- IFCDeliveryValidator 규칙 JSON 배포 -->
  <ItemGroup>
{rel_cfg_items}
  </ItemGroup>
"""

    # ClosedXML + System.Net.Http 추가 (없으면)
    pkg_insert = ""
    if "ClosedXML" not in content:
        pkg_insert = '    <PackageReference Include="ClosedXML" Version="0.102.1" />\n'

    # <PackageReference Include="Newtonsoft.Json"> 바로 뒤에 삽입
    old_pkg = '    <PackageReference Include="Newtonsoft.Json"        Version="13.0.3" />'
    new_pkg = old_pkg + "\n" + pkg_insert.rstrip("\n")
    if pkg_insert:
        content = content.replace(old_pkg, new_pkg)

    # </Project> 직전에 새 ItemGroup 삽입
    content = content.replace("</Project>", additions + "</Project>")

    csproj.write_text(content, encoding="utf-8")
    print(f"  .csproj 업데이트 완료 (ClosedXML {'추가' if pkg_insert else '이미 있음'})")
    return [csproj]


# ═════════════════════════════════════════════════════════════════
# 2  WiX Installer 템플릿
# ═════════════════════════════════════════════════════════════════
async def build_wix_installer() -> list[Path]:
    out = ADDIN_DASH / "Installer" / "WiX"
    out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []

    files.append(write(out / "BIMCommandCenter.wxs", r"""
<?xml version="1.0" encoding="UTF-8"?>
<!--
  BIM Command Center for Revit — WiX v4 Installer
  빌드: wix build BIMCommandCenter.wxs -o BIMCommandCenter.msi
  요구: WiX Toolset v4.x  (dotnet tool install -g wix)
-->
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">

  <Package Name="BIM Command Center for Revit"
           Manufacturer="LUA BIM LABS"
           Version="!(bind.FileVersion.MainDll)"
           UpgradeCode="A1B2C3D4-E5F6-7890-ABCD-EF1234567890"
           Scope="perMachine">

    <MajorUpgrade DowngradeErrorMessage="더 최신 버전이 이미 설치되어 있습니다." />
    <MediaTemplate EmbedCab="yes" />

    <Feature Id="ProductFeature" Title="BIM Command Center" Level="1">
      <ComponentGroupRef Id="RevitAddinFiles" />
      <ComponentGroupRef Id="AddinManifests_2024" />
      <ComponentGroupRef Id="AddinManifests_2025" />
      <ComponentGroupRef Id="AddinManifests_2026" />
    </Feature>
  </Package>

  <!-- DLL 공유 폴더 -->
  <Fragment>
    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramData64Folder">
        <Directory Id="AutodeskDir" Name="Autodesk">
          <Directory Id="RevitAddinsDir" Name="Revit">
            <Directory Id="AddinsRoot" Name="Addins">
              <Directory Id="BCCDir" Name="BIMCommandCenter">
                <Directory Id="Net48Dir"  Name="net48"/>
                <Directory Id="Net8Dir"   Name="net8.0-windows"/>
              </Directory>
            </Directory>
          </Directory>
        </Directory>
      </Directory>
    </Directory>

    <ComponentGroup Id="RevitAddinFiles" Directory="Net48Dir">
      <Component Id="MainDll" Guid="*">
        <File Id="MainDll" Source="$(var.OutDir)net48\BIMCommandCenter.dll"
              KeyPath="yes" />
      </Component>
      <Component Id="ClosedXML" Guid="*">
        <File Id="ClosedXMLDll" Source="$(var.OutDir)net48\ClosedXML.dll" KeyPath="yes"/>
      </Component>
      <Component Id="NewtonsoftJson" Guid="*">
        <File Id="NewtonsoftDll" Source="$(var.OutDir)net48\Newtonsoft.Json.dll" KeyPath="yes"/>
      </Component>
      <!-- IFC 검증 규칙 JSON -->
      <Component Id="IFCRulesJson" Guid="*" Directory="Net48Dir">
        <File Id="IFCRules" KeyPath="yes"
              Source="$(var.ProjectDir)..\\IFCDeliveryValidator\\Configs\\korea_bim_delivery_rules.json"/>
      </Component>
    </ComponentGroup>

    <!-- Revit 2024 .addin 등록 -->
    <ComponentGroup Id="AddinManifests_2024">
      <Component Id="Addin2024" Guid="*"
                 Directory="TARGETDIR"
                 Condition="REVIT2024INSTALLED">
        <File Id="AddinFile2024" KeyPath="yes"
              Source="$(var.ProjectDir)addin\BIMCommandCenter.addin"
              Name="BIMCommandCenter.addin" />
        <RegistryValue Root="HKLM"
                       Key="SOFTWARE\LUA BIM LABS\BIMCommandCenter"
                       Name="Revit2024Installed" Value="1" Type="integer"/>
      </Component>
    </ComponentGroup>

    <!-- Revit 2025/2026도 동일 패턴 -->
    <ComponentGroup Id="AddinManifests_2025">
      <Component Id="Addin2025" Guid="*" Directory="TARGETDIR"
                 Condition="REVIT2025INSTALLED">
        <File Id="AddinFile2025" KeyPath="yes"
              Source="$(var.ProjectDir)addin\BIMCommandCenter_net8.addin"
              Name="BIMCommandCenter.addin"/>
      </Component>
    </ComponentGroup>
    <ComponentGroup Id="AddinManifests_2026">
      <Component Id="Addin2026" Guid="*" Directory="TARGETDIR"
                 Condition="REVIT2026INSTALLED">
        <File Id="AddinFile2026" KeyPath="yes"
              Source="$(var.ProjectDir)addin\BIMCommandCenter_net8.addin"
              Name="BIMCommandCenter.addin"/>
      </Component>
    </ComponentGroup>
  </Fragment>

  <!-- Revit 설치 감지 -->
  <Fragment>
    <Property Id="REVIT2024INSTALLED">
      <RegistrySearch Id="Revit2024Reg" Root="HKLM"
                      Key="SOFTWARE\\Autodesk\\Revit\\2024"
                      Name="InstallationPath" Type="raw"/>
    </Property>
    <Property Id="REVIT2025INSTALLED">
      <RegistrySearch Id="Revit2025Reg" Root="HKLM"
                      Key="SOFTWARE\\Autodesk\\Revit\\2025"
                      Name="InstallationPath" Type="raw"/>
    </Property>
    <Property Id="REVIT2026INSTALLED">
      <RegistrySearch Id="Revit2026Reg" Root="HKLM"
                      Key="SOFTWARE\\Autodesk\\Revit\\2026"
                      Name="InstallationPath" Type="raw"/>
    </Property>
  </Fragment>

</Wix>
"""))

    files.append(write(out / "build_installer.ps1", r"""
# BIM Command Center MSI 빌드 스크립트
# 실행: .\build_installer.ps1 [-Version "1.2.0"]
param([string]$Version = "1.0.0")

$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent | Split-Path -Parent

Write-Host "=== BIM Command Center Installer Build v$Version ===" -ForegroundColor Cyan

# 1. .NET 빌드
dotnet build "$Root\BIMCommandCenter.csproj" -c Release -f net48
dotnet build "$Root\BIMCommandCenter.csproj" -c Release -f net8.0-windows

# 2. WiX MSI 빌드
wix build "$PSScriptRoot\BIMCommandCenter.wxs" `
    -d "Version=$Version" `
    -d "OutDir=$Root\bin\Release\" `
    -d "ProjectDir=$Root\" `
    -o "$Root\dist\BIMCommandCenter_v$Version.msi"

Write-Host "MSI 생성: $Root\dist\BIMCommandCenter_v$Version.msi" -ForegroundColor Green
"""))
    print(f"  [WIX] Installer 템플릿 — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# 3  License Gate 통합
# ═════════════════════════════════════════════════════════════════
async def build_license_gate() -> list[Path]:
    out = ADDIN_DASH / "Services"
    files: list[Path] = []

    files.append(write(out / "CommandLicenseGate.cs", """\
using Autodesk.Revit.UI;
using BIMCommandCenter.License;

namespace BIMCommandCenter.Services
{
    /// <summary>
    /// 커맨드 실행 전 라이선스 유효성을 확인하는 게이트.
    /// 모든 신규 IExternalCommand 의 Execute() 첫 줄에서 호출한다.
    /// </summary>
    public static class CommandLicenseGate
    {
        /// <summary>라이선스 유효 여부. false 이면 커맨드를 즉시 Result.Failed로 반환.</summary>
        public static bool Check(Autodesk.Revit.ApplicationServices.ControlledApplication app,
            out string reason)
        {
            if (LicenseManager.IsActivated(app, out reason))
                return true;
            TaskDialog.Show("BIM Command Center — 라이선스",
                $"이 기능을 사용하려면 유효한 라이선스가 필요합니다.\\n\\n{reason}\\n\\n" +
                "구독 정보: https://luabimlabs.com/bcc");
            return false;
        }

        /// <summary>UIApplication 오버로드 (실행 중 체크용)</summary>
        public static bool Check(UIApplication uiApp, out string reason)
            => Check(uiApp.Application.Application, out reason);
    }
}
"""))

    # 기존 커맨드들에 라이선스 게이트를 일괄 추가하는 코드 조각 (주석 형태로 가이드)
    files.append(write(ADDIN_DASH / "docs" / "license_gate_integration.md", """\
# License Gate 통합 가이드

모든 신규 IExternalCommand 의 `Execute()` 메서드 첫 줄에 아래 코드를 추가하세요:

```csharp
// 라이선스 확인
if (!CommandLicenseGate.Check(data.Application.Application, out string licReason))
{
    message = licReason;
    return Result.Failed;
}
```

## 적용 대상 커맨드 목록
- TagTextAlignerCommand
- ViewTemplateCopierCommand
- TypeBatchDefinerCommand
- ElementRenumberingCommand
- ProjectCleanupCommand
- LineCleanupCommand
- SmartSelectorCommand
- WorksetInspectorCommand
- LinkHealthCommand
- ScheduleExportCommand
- ScheduleExcelSyncCommand
- MEPLengthCommand
- WarningManagerCommand
- BatchPrintCommand
- SheetViewDuplicatorCommand
- RoomFinishingCommand
- IFCDeliveryValidatorCommand
- MultiMaterialTaggerCommand
- FamilyPackageTransferCommand

## 무료 기능 (라이선스 불필요)
- Settings Profile Manager (설정 전용, 모델 변경 없음)
"""))
    print(f"  [LICENSE] CommandLicenseGate — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# 4  AutoUpdateChecker
# ═════════════════════════════════════════════════════════════════
async def build_auto_update() -> list[Path]:
    out = ADDIN_DASH / "Services"
    files: list[Path] = []

    files.append(write(out / "AutoUpdateChecker.cs", """\
using Newtonsoft.Json;
using System;
using System.Net.Http;
using System.Reflection;
using System.Threading.Tasks;
using System.Windows;

namespace BIMCommandCenter.Services
{
    /// <summary>
    /// 애드인 시작 시 최신 버전 여부를 백그라운드로 확인.
    /// 새 버전 발견 시 TaskDialog 알림.
    /// </summary>
    public static class AutoUpdateChecker
    {
        private const string UpdateUrl =
            "https://luabimlabs.com/api/bcc/latest-version";

        private static readonly HttpClient _http = new HttpClient
            { Timeout = TimeSpan.FromSeconds(5) };

        public static Version CurrentVersion
            => Assembly.GetExecutingAssembly().GetName().Version
               ?? new Version(1, 0, 0);

        /// <summary>비동기 버전 체크 — 실패 시 조용히 무시.</summary>
        public static async Task CheckAsync()
        {
            try
            {
                var json    = await _http.GetStringAsync(UpdateUrl);
                var payload = JsonConvert.DeserializeAnonymousType(json,
                    new { version = "", download_url = "", release_notes = "" });

                if (payload == null || string.IsNullOrEmpty(payload.version)) return;

                if (Version.TryParse(payload.version, out var latest)
                    && latest > CurrentVersion)
                {
                    // UI 스레드에서 알림
                    System.Windows.Application.Current?.Dispatcher?.Invoke(() =>
                    {
                        var td = new Autodesk.Revit.UI.TaskDialog("BIM Command Center 업데이트");
                        td.MainContent    = $"새 버전 {payload.version} 이 출시되었습니다.\n" +
                                           $"현재 버전: {CurrentVersion}";
                        td.ExpandedContent = payload.release_notes;
                        td.CommonButtons  = Autodesk.Revit.UI.TaskDialogCommonButtons.Ok;
                        td.Show();
                    });
                }
            }
            catch { /* 네트워크 오류 시 조용히 무시 */ }
        }

        /// <summary>동기 래퍼 (OnStartup에서 호출).</summary>
        public static void CheckInBackground()
            => Task.Run(CheckAsync);
    }
}
"""))
    print(f"  [UPDATE] AutoUpdateChecker — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# 5  PowerShell 빌드 스크립트
# ═════════════════════════════════════════════════════════════════
async def build_ps1_script() -> list[Path]:
    out = ADDIN_DASH
    files: list[Path] = []

    files.append(write(out / "build_all.ps1", r"""
# BIM Command Center 전체 빌드 + 배포 스크립트
# 실행: .\build_all.ps1 [-Config Release] [-Version "1.0.0"]
param(
    [string]$Config   = "Release",
    [string]$Version  = "1.0.0",
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"
$Root    = $PSScriptRoot
$OutDir  = "$Root\dist"
$LogFile = "$Root\build_$($Config)_$(Get-Date -Format 'yyyyMMdd_HHmm').log"

function Log($msg) { Write-Host $msg -ForegroundColor Cyan; Add-Content $LogFile $msg }

Log "=== BIM Command Center Build v$Version ($Config) ==="
Log "시작: $(Get-Date)"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# 1. .NET Framework 4.8 빌드 (Revit 2019~2024)
Log "[1/4] net48 빌드..."
dotnet build "$Root\BIMCommandCenter.csproj" `
    -c $Config -f net48 `
    /p:AssemblyVersion=$Version `
    /p:FileVersion=$Version `
    | Tee-Object -FilePath $LogFile -Append

# 2. .NET 8 빌드 (Revit 2025~2027)
Log "[2/4] net8.0-windows 빌드..."
dotnet build "$Root\BIMCommandCenter.csproj" `
    -c $Config -f net8.0-windows `
    /p:AssemblyVersion=$Version `
    /p:FileVersion=$Version `
    | Tee-Object -FilePath $LogFile -Append

# 3. 테스트 (선택)
if (-not $SkipTests) {
    Log "[3/4] 테스트 실행..."
    $testProject = "$Root\..\BIMCommandCenter.Tests\BIMCommandCenter.Tests.csproj"
    if (Test-Path $testProject) {
        dotnet test $testProject --no-build -c $Config `
            | Tee-Object -FilePath $LogFile -Append
    } else {
        Log "  테스트 프로젝트 없음 — 스킵"
    }
} else {
    Log "[3/4] 테스트 스킵 (-SkipTests)"
}

# 4. MSI 패키징 (WiX 설치된 경우)
Log "[4/4] MSI 패키징..."
$wixScript = "$Root\Installer\WiX\build_installer.ps1"
if (Test-Path $wixScript) {
    & $wixScript -Version $Version
    Log "  MSI: $OutDir\BIMCommandCenter_v$Version.msi"
} else {
    Log "  WiX 스크립트 없음 — 스킵"
}

Log ""
Log "=== 빌드 완료: $(Get-Date) ==="
Log "로그: $LogFile"
"""))

    files.append(write(out / "deploy_addin.ps1", r"""
# 개발 PC → Revit 애드인 빠른 배포 스크립트
# 실행: .\deploy_addin.ps1 (Revit 닫은 후 실행)
$Root     = $PSScriptRoot
$DllDir   = "$Root\bin\Release\net48"
$DllDir8  = "$Root\bin\Release\net8.0-windows"
$AddinSrc = "$Root\addin\BIMCommandCenter.addin"

$RevitYears = @{
    "2024" = "net48";
    "2025" = "net8.0-windows";
    "2026" = "net8.0-windows";
}

foreach ($year in $RevitYears.Keys) {
    $addinFolder = "C:\ProgramData\Autodesk\Revit\Addins\$year"
    $dllFolder   = "C:\ProgramData\Autodesk\Revit\Addins\BIMCommandCenter\$($RevitYears[$year])"
    if (-not (Test-Path $addinFolder)) { Write-Host "Revit $year 없음 — 스킵"; continue }

    New-Item -ItemType Directory -Force -Path $dllFolder | Out-Null
    $src = if ($RevitYears[$year] -eq "net48") { $DllDir } else { $DllDir8 }
    Copy-Item "$src\*.dll" $dllFolder -Force
    Copy-Item "$src\*.json" $dllFolder -Force -ErrorAction SilentlyContinue
    Copy-Item $AddinSrc "$addinFolder\BIMCommandCenter.addin" -Force
    Write-Host "Revit $year 배포 완료" -ForegroundColor Green
}
"""))
    print(f"  [BUILD] PowerShell 빌드 스크립트 — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# 6  Navisworks .csproj 스캐폴드 (N-01/02/03/05)
# ═════════════════════════════════════════════════════════════════
async def build_nw_csproj() -> list[Path]:
    files: list[Path] = []

    nw_projects = [
        ("ClashResponsibilityBoard", "NavisworksClashBoard",
         ["ClashItem.cs","ClashGrouper.cs","ClashBoardForm.cs",
          "ClashResponsibilityPlugin.cs","ReportGenerator.cs","ResponsibilityRule.cs"]),
        ("ClashGroupEngine", "NavisworksClashGroup",
         ["ClashGroupEngine.cs","ClashGroupForm.cs","ClashGroupPlugin.cs","ClashGroupRule.cs"]),
        ("ClashTestDefiner", "NavisworksClashDefiner",
         ["ClashTestDefinerEngine.cs","ClashTestDefinerForm.cs",
          "ClashTestDefinerPlugin.cs","ClashTestDefinition.cs"]),
        ("IFCExportHelper", "NavisworksIFCExport",
         ["IFCExportConfig.cs","IFCExportEngine.cs","IFCExportForm.cs","IFCExportPlugin.cs"]),
    ]

    nw_api_path = r"C:\Program Files\Autodesk\Navisworks Manage 2025"

    for folder, ns, src_files in nw_projects:
        out = NAV_ROOT / folder
        out.mkdir(parents=True, exist_ok=True)

        includes = "\n".join(f'    <Compile Include="src\\{f}" />' for f in src_files)
        csproj_content = f"""\
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net48</TargetFramework>
    <AssemblyName>{folder}</AssemblyName>
    <RootNamespace>{ns}</RootNamespace>
    <PlatformTarget>x64</PlatformTarget>
    <LangVersion>9</LangVersion>
    <UseWindowsForms>true</UseWindowsForms>
    <Nullable>disable</Nullable>
  </PropertyGroup>

  <!-- Navisworks API -->
  <ItemGroup>
    <Reference Include="Autodesk.Navisworks.Api">
      <HintPath>{nw_api_path}\\Autodesk.Navisworks.Api.dll</HintPath>
      <Private>false</Private>
    </Reference>
    <Reference Include="Autodesk.Navisworks.Clash">
      <HintPath>{nw_api_path}\\Autodesk.Navisworks.Clash.dll</HintPath>
      <Private>false</Private>
    </Reference>
    <Reference Include="Autodesk.Navisworks.Interop.ComApi">
      <HintPath>{nw_api_path}\\Autodesk.Navisworks.Interop.ComApi.dll</HintPath>
      <Private>false</Private>
    </Reference>
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="ClosedXML"       Version="0.102.1" />
  </ItemGroup>

  <!-- 공통 레이어 -->
  <ItemGroup>
    <Compile Include="..\_Shared\\KoreanReport\\KoreanReportGenerator.cs" />
    <Compile Include="..\_Shared\\KoreanReport\\NavisworksHelper.cs" />
  </ItemGroup>

  <!-- 소스 파일 -->
  <ItemGroup>
{includes}
  </ItemGroup>

  <Target Name="CopyToNavisworks" AfterTargets="Build">
    <PropertyGroup>
      <NWPluginDir>{nw_api_path}\\Plugins\\{folder}\\</NWPluginDir>
    </PropertyGroup>
    <MakeDir Directories="$(NWPluginDir)" />
    <Copy SourceFiles="$(TargetPath)"         DestinationFolder="$(NWPluginDir)" ContinueOnError="true"/>
    <Copy SourceFiles="$(TargetDir)ClosedXML.dll"       DestinationFolder="$(NWPluginDir)" ContinueOnError="true"/>
    <Copy SourceFiles="$(TargetDir)Newtonsoft.Json.dll" DestinationFolder="$(NWPluginDir)" ContinueOnError="true"/>
    <Copy SourceFiles="$(ProjectDir){folder}.addinmanifest" DestinationFolder="$(NWPluginDir)" ContinueOnError="true"/>
  </Target>
</Project>
"""
        p = write(out / f"{folder}.csproj", csproj_content)
        files.append(p)

    # Navisworks 솔루션 파일
    guids = {
        "ClashResponsibilityBoard": "AAA11111-1111-1111-1111-111111111111",
        "ClashGroupEngine":          "BBB22222-2222-2222-2222-222222222222",
        "ClashTestDefiner":          "CCC33333-3333-3333-3333-333333333333",
        "IFCExportHelper":           "DDD44444-4444-4444-4444-444444444444",
    }
    sln_projects = "\n".join(
        f'Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{f}", '
        f'"{f}\\\\{f}.csproj", "{{{g}}}"\nEndProject'
        for f, g in guids.items()
    )
    sln = f"""\

Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.0.0.0
{sln_projects}
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        Release|x64 = Release|x64
        Debug|x64   = Debug|x64
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution
"""
    for g in guids.values():
        sln += (f"        {{{g}}}.Release|x64.ActiveCfg = Release|x64\n"
                f"        {{{g}}}.Release|x64.Build.0   = Release|x64\n"
                f"        {{{g}}}.Debug|x64.ActiveCfg   = Debug|x64\n"
                f"        {{{g}}}.Debug|x64.Build.0     = Debug|x64\n")
    sln += "    EndGlobalSection\nEndGlobal\n"

    files.append(write(NAV_ROOT / "NavisworksAddins.sln", sln))
    print(f"  [NW-CSPROJ] Navisworks 프로젝트 파일 — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# 7  Settings Profile UI 강화
# ═════════════════════════════════════════════════════════════════
async def build_settings_ui() -> list[Path]:
    out = ADDIN_DASH / "UI"
    files: list[Path] = []

    files.append(write(out / "SettingsProfileWindow.xaml.cs", """\
using BIMCommandCenter.CommercialFeatures.Services;
using Microsoft.Win32;
using System.IO;
using System.Windows;

namespace BIMCommandCenter.UI
{
    /// <summary>설정 프로파일 관리 WPF 창</summary>
    public partial class SettingsProfileWindow : Window
    {
        public SettingsProfileWindow()
        {
            InitializeComponent();
            Refresh();
        }

        private void Refresh()
        {
            var profiles = CommercialFeatureConfigService.ListProfiles();
            LstProfiles.ItemsSource = profiles;
            TxtProfileDir.Text      = CommercialFeatureConfigService.UserProfileDirectory;
        }

        private void BtnLoad_Click(object s, RoutedEventArgs e)
        {
            if (LstProfiles.SelectedItem is not ProfileEntry entry) return;
            try
            {
                var profile = CommercialFeatureConfigService.LoadJson<
                    BIMCommandCenter.CommercialFeatures.Models.SettingsProfile>(entry.Path);
                TxtStatus.Text = $"로드 완료: {profile.ProfileName} (v{profile.ProfileVersion})";
            }
            catch (System.Exception ex) { TxtStatus.Text = $"오류: {ex.Message}"; }
        }

        private void BtnNewOffice_Click(object s, RoutedEventArgs e)
        {
            var dlg = new SaveFileDialog
            {
                InitialDirectory = CommercialFeatureConfigService.UserProfileDirectory,
                Filter = "JSON 프로파일 (*.json)|*.json",
                FileName = "office_profile.json",
            };
            if (dlg.ShowDialog() != true) return;
            CreateDefaultProfile(dlg.FileName, "office");
            Refresh();
        }

        private void BtnNewProject_Click(object s, RoutedEventArgs e)
        {
            var dlg = new SaveFileDialog
            {
                InitialDirectory = CommercialFeatureConfigService.UserProfileDirectory,
                Filter = "JSON 프로파일 (*.json)|*.json",
                FileName = "project_profile.json",
            };
            if (dlg.ShowDialog() != true) return;
            CreateDefaultProfile(dlg.FileName, "project");
            Refresh();
        }

        private static void CreateDefaultProfile(string path, string scope)
        {
            var sample = new
            {
                feature         = "settings_profile",
                version         = 1,
                profile_name    = System.IO.Path.GetFileNameWithoutExtension(path),
                profile_version = 1,
                scope,
                product         = "BIM Command Center",
                features        = new { tag_text_aligner = new { default_mode = "AlignLeft" } },
            };
            File.WriteAllText(path,
                Newtonsoft.Json.JsonConvert.SerializeObject(sample,
                    Newtonsoft.Json.Formatting.Indented));
        }

        private void BtnOpenDir_Click(object s, RoutedEventArgs e)
        {
            var dir = CommercialFeatureConfigService.UserProfileDirectory;
            System.Diagnostics.Process.Start("explorer.exe", dir);
        }

        private void BtnClose_Click(object s, RoutedEventArgs e) => Close();
    }

    public class ProfileEntry
    {
        public string Name { get; set; }
        public string Path { get; set; }
        public string Scope { get; set; }
    }
}
"""))

    files.append(write(out / "SettingsProfileWindow.xaml", """\
<Window x:Class="BIMCommandCenter.UI.SettingsProfileWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Settings Profile Manager" Height="420" Width="520"
        WindowStartupLocation="CenterScreen">
    <Grid Margin="12">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>
        <StackPanel Grid.Row="0" Orientation="Horizontal" Margin="0,0,0,8">
            <TextBlock Text="프로파일 폴더:" VerticalAlignment="Center" Width="100"/>
            <TextBlock x:Name="TxtProfileDir" VerticalAlignment="Center"
                       FontSize="11" Foreground="Gray" TextWrapping="NoWrap"
                       TextTrimming="CharacterEllipsis" MaxWidth="320"/>
            <Button Content="열기" Margin="8,0,0,0" Padding="4,2" Click="BtnOpenDir_Click"/>
        </StackPanel>
        <ListBox Grid.Row="1" x:Name="LstProfiles" DisplayMemberPath="Name"
                 Margin="0,0,0,8"/>
        <TextBlock Grid.Row="2" x:Name="TxtStatus" Margin="0,0,0,8"
                   Foreground="DarkBlue" TextWrapping="Wrap"/>
        <StackPanel Grid.Row="3" Orientation="Horizontal" Margin="0,0,0,8">
            <Button Content="로드"          Width="80" Margin="0,0,4,0" Click="BtnLoad_Click"/>
            <Button Content="Office 신규"   Width="90" Margin="0,0,4,0" Click="BtnNewOffice_Click"/>
            <Button Content="Project 신규"  Width="90" Margin="0,0,4,0" Click="BtnNewProject_Click"/>
        </StackPanel>
        <StackPanel Grid.Row="4" Orientation="Horizontal" HorizontalAlignment="Right">
            <Button Content="닫기" Width="80" Click="BtnClose_Click"/>
        </StackPanel>
    </Grid>
</Window>
"""))
    print(f"  [SETTINGS-UI] SettingsProfileWindow — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# 8  CommandLaunchHandler 확장 (신규 커맨드 라우팅)
# ═════════════════════════════════════════════════════════════════
async def extend_command_launch_handler() -> list[Path]:
    out = ADDIN_DASH / "Services"
    files: list[Path] = []

    files.append(write(out / "NewCommandRouter.cs", """\
using Autodesk.Revit.UI;
using BIMCommandCenter.Commands;
using System;
using System.Collections.Generic;

namespace BIMCommandCenter.Services
{
    /// <summary>
    /// DashboardView 의 커맨드 버튼 클릭 → 신규 IExternalCommand 실행 라우터.
    /// CommandLaunchHandler 와 함께 사용한다.
    /// </summary>
    public static class NewCommandRouter
    {
        private static readonly Dictionary<string, Func<ExternalCommandData, Result>> _routes
            = new Dictionary<string, Func<ExternalCommandData, Result>>(StringComparer.OrdinalIgnoreCase)
        {
            ["TAG_TEXT_ALIGNER"]     = d => RunCommand<TagTextAlignerCommand>(d),
            ["LINE_CLEANUP"]         = d => RunCommand<LineCleanupCommand>(d),
            ["VIEW_TEMPLATE_COPIER"] = d => RunCommand<ViewTemplateCopierCommand>(d),
            ["SMART_SELECTOR"]       = d => RunCommand<SmartSelectorCommand>(d),
            ["WORKSET_INSPECTOR"]    = d => RunCommand<WorksetInspectorCommand>(d),
            ["SHEET_DUPLICATOR"]     = d => RunCommand<SheetViewDuplicatorCommand>(d),
            ["TYPE_BATCH_DEFINER"]   = d => RunCommand<TypeBatchDefinerCommand>(d),
            ["ELEMENT_RENUMBERING"]  = d => RunCommand<ElementRenumberingCommand>(d),
            ["PROJECT_CLEANUP"]      = d => RunCommand<ProjectCleanupCommand>(d),
            ["WARNING_MANAGER"]      = d => RunCommand<WarningManagerCommand>(d),
            ["ROOM_FINISHING"]       = d => RunCommand<RoomFinishingCommand>(d),
            ["MULTI_MATERIAL_TAG"]   = d => RunCommand<MultiMaterialTaggerCommand>(d),
            ["FAMILY_TRANSFER"]      = d => RunCommand<FamilyPackageTransferCommand>(d),
            ["SCHEDULE_EXPORT"]      = d => RunCommand<ScheduleExportCommand>(d),
            ["SCHEDULE_SYNC"]        = d => RunCommand<ScheduleExcelSyncCommand>(d),
            ["IFC_VALIDATOR"]        = d => RunCommand<IFCDeliveryValidatorCommand>(d),
            ["MEP_LENGTH"]           = d => RunCommand<MEPLengthCommand>(d),
            ["LINK_HEALTH"]          = d => RunCommand<LinkHealthCommand>(d),
            ["BATCH_PRINT"]          = d => RunCommand<BatchPrintCommand>(d),
        };

        public static bool TryRoute(string commandId, ExternalCommandData data, out Result result)
        {
            if (_routes.TryGetValue(commandId, out var fn))
            {
                result = fn(data);
                return true;
            }
            result = Result.Failed;
            return false;
        }

        private static Result RunCommand<T>(ExternalCommandData data)
            where T : Autodesk.Revit.UI.IExternalCommand, new()
        {
            string msg = "";
            var els = new Autodesk.Revit.DB.ElementSet();
            return new T().Execute(data, ref msg, els);
        }
    }
}
"""))
    print(f"  [ROUTER] NewCommandRouter — {len(files)}개")
    return files


# ═════════════════════════════════════════════════════════════════
# 메인
# ═════════════════════════════════════════════════════════════════
async def main():
    print(f"BCC Add-in 5차 개발 러너 (인프라·빌드·통합) — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    batches = [
        ("CSPROJ",   "BIMCommandCenter.csproj 업데이트",      "통합",  update_csproj),
        ("WIX",      "WiX Installer + 빌드 스크립트",         "배포",  build_wix_installer),
        ("LICENSE",  "CommandLicenseGate 통합",               "보안",  build_license_gate),
        ("UPDATE",   "AutoUpdateChecker",                     "서비스", build_auto_update),
        ("BUILD",    "PowerShell 빌드·배포 스크립트",          "DevOps", build_ps1_script),
        ("NW-PROJ",  "Navisworks .csproj + .sln",             "Navisworks", build_nw_csproj),
        ("SETTINGS", "Settings Profile UI 강화",               "UX",    build_settings_ui),
        ("ROUTER",   "NewCommandRouter (커맨드 라우팅)",        "통합",  extend_command_launch_handler),
    ]

    for item_id, display, kind, builder in batches:
        print(f"\n{'='*55}\n[{item_id}] {display}\n{'='*55}")
        files = await builder()
        if files:
            mail(item_id, display, kind, files)
            print(f"  ✓ 이메일 발송")

    print(f"\n\n5차 개발 전체 완료")


if __name__ == "__main__":
    asyncio.run(main())
