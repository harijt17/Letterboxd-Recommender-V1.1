; ============================================================
; Letterboxd Recommender Installer
; ============================================================

#define MyAppName "Letterboxd Recommender"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "HariPrasath JT"
#define MyAppExeName "Letterboxd Recommender.exe"
#define MyInstallerName "Letterboxd_Recommender_Setup_v2.0.0"

[Setup]

AppId={{7D28CF5B-92D2-4A56-91E5-44B2CFA6F5D1}

AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

OutputDir=..\release
OutputBaseFilename=Letterboxd_Recommender_Setup_v2.0.0

SetupIconFile=icon.ico

WizardStyle=modern

Compression=lzma2
SolidCompression=yes

PrivilegesRequired=admin

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableDirPage=no
DisableProgramGroupPage=yes

UninstallDisplayIcon={app}\{#MyAppExeName}


[Languages]

Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]

Name: "desktopicon"; \
Description: "Create a Desktop Shortcut"; \
GroupDescription: "Additional Icons:"


[Files]

Source: "..\dist\launcher.dist\*"; \
DestDir: "{app}"; \
Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]

Name: "{autoprograms}\{#MyAppName}"; \
Filename: "{app}\{#MyAppExeName}"

Name: "{autodesktop}\{#MyAppName}"; \
Filename: "{app}\{#MyAppExeName}"; \
Tasks: desktopicon


[Run]

Filename: "{app}\{#MyAppExeName}"; \
Description: "Launch {#MyAppName}"; \
Flags: nowait postinstall skipifsilent