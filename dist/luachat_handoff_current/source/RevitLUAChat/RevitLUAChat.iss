#define AppName "LUA BIM LABS Revit Assistant"
#define AppVersion "1.2.1"
#define AppPublisher "S-TEC D&D"
#define AppGUID "A1B2C3D4-E5F6-7890-ABCD-EF1234567890"

[Setup]
AppId={{{#AppGUID}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL=https://www.s-tec.co.kr
DefaultDirName={commonappdata}\LUA BIM LABS\RevitLUAChat
DisableDirPage=yes
CreateAppDir=yes
OutputDir=installer
OutputBaseFilename=RevitLUAChat_Setup_v{#AppVersion}
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern
UninstallDisplayName={#AppName} for Revit
UninstallDisplayIcon={app}\net48\RevitLUAChat.dll
MinVersion=6.1sp1
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Files]
Source: "bin\Release\net48\RevitLUAChat.dll"; DestDir: "{app}\net48"; Flags: ignoreversion
Source: "bin\Release\net48\Newtonsoft.Json.dll"; DestDir: "{app}\net48"; Flags: ignoreversion

Source: "bin\Release\net8.0-windows\RevitLUAChat.dll"; DestDir: "{app}\net8"; Flags: ignoreversion
Source: "bin\Release\net8.0-windows\Newtonsoft.Json.dll"; DestDir: "{app}\net8"; Flags: ignoreversion skipifsourcedoesntexist
Source: "bin\Release\net8.0-windows\RevitLUAChat.deps.json"; DestDir: "{app}\net8"; Flags: ignoreversion skipifsourcedoesntexist

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "LUA_BIM_LABS_BACKEND_URL"; ValueData: "{code:GetBackendUrl}"; Flags: preservestringtype uninsdeletevalue

[Code]

const
  ADDIN_GUID = 'A1B2C3D4-E5F6-7890-ABCD-EF1234567890';

function GetBackendUrl(Param: String): String;
begin
  Result := Trim(ExpandConstant('{param:BackendUrl|http://127.0.0.1:8000}'));
  if Result = '' then
    Result := 'http://127.0.0.1:8000';
end;

function IsRevitInstalled(Year: Integer): Boolean;
var
  RevitExe: String;
  AddinsDir: String;
begin
  RevitExe := 'C:\Program Files\Autodesk\Revit ' + IntToStr(Year) + '\Revit.exe';
  AddinsDir := ExpandConstant('{commonappdata}') + '\Autodesk\Revit\Addins\' + IntToStr(Year);
  Result := FileExists(RevitExe) or DirExists(AddinsDir);
end;

procedure WriteAddinFile(Year: Integer; DllPath: String);
var
  AddinDir: String;
  AddinFile: String;
  Lines: TArrayOfString;
begin
  AddinDir := ExpandConstant('{commonappdata}') + '\Autodesk\Revit\Addins\' + IntToStr(Year);
  AddinFile := AddinDir + '\RevitLUAChat.addin';

  if not DirExists(AddinDir) then
    ForceDirectories(AddinDir);

  SetArrayLength(Lines, 11);
  Lines[0]  := '<?xml version="1.0" encoding="utf-8"?>';
  Lines[1]  := '<RevitAddIns>';
  Lines[2]  := '  <AddIn Type="Application">';
  Lines[3]  := '    <Name>RevitLUAChat</Name>';
  Lines[4]  := '    <Assembly>' + DllPath + '</Assembly>';
  Lines[5]  := '    <AddInId>' + ADDIN_GUID + '</AddInId>';
  Lines[6]  := '    <FullClassName>RevitLUAChat.App</FullClassName>';
  Lines[7]  := '    <VendorId>STEC</VendorId>';
  Lines[8]  := '    <VendorDescription>LUA BIM LABS</VendorDescription>';
  Lines[9]  := '  </AddIn>';
  Lines[10] := '</RevitAddIns>';

  SaveStringsToFile(AddinFile, Lines, False);
end;

procedure RemoveAddinFile(Year: Integer);
var
  AddinFile: String;
begin
  AddinFile := ExpandConstant('{commonappdata}') + '\Autodesk\Revit\Addins\' + IntToStr(Year) + '\RevitLUAChat.addin';
  if FileExists(AddinFile) then
    DeleteFile(AddinFile);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  AppDir: String;
  Net48Dll: String;
  Net8Dll: String;
  Year: Integer;
  InstalledVersions: String;
begin
  if CurStep = ssPostInstall then
  begin
    AppDir := ExpandConstant('{app}');
    Net48Dll := AppDir + '\net48\RevitLUAChat.dll';
    Net8Dll := AppDir + '\net8\RevitLUAChat.dll';
    InstalledVersions := '';

    for Year := 2019 to 2024 do
    begin
      if IsRevitInstalled(Year) then
      begin
        WriteAddinFile(Year, Net48Dll);
        InstalledVersions := InstalledVersions + ' ' + IntToStr(Year);
      end;
    end;

    for Year := 2025 to 2026 do
    begin
      if IsRevitInstalled(Year) then
      begin
        WriteAddinFile(Year, Net8Dll);
        InstalledVersions := InstalledVersions + ' ' + IntToStr(Year);
      end;
    end;

    if InstalledVersions <> '' then
      MsgBox(
        'LUA BIM LABS Revit Assistant was installed for Revit versions:' + #13#10 + Trim(InstalledVersions) + #13#10#13#10 +
        'Backend URL was configured automatically:' + #13#10 + GetBackendUrl('') + #13#10#13#10 +
        'Restart Revit to load the add-in.',
        mbInformation,
        MB_OK)
    else
      MsgBox(
        'No supported Revit installation was detected.' + #13#10 +
        'You can still install the add-in manifest manually later.',
        mbInformation,
        MB_OK);

  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  Year: Integer;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    for Year := 2019 to 2026 do
      RemoveAddinFile(Year);
  end;
end;
