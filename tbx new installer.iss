; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "TBX"
#define MyAppVersion "2.1"
#define MyAppPublisher "TBX"
#define MyAppExeName "main.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{B2996495-701D-43AF-95D0-31AB8D9DA89D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputBaseFilename=TBX setup
SetupIconFile=C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\assets\tbx_logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "armenian"; MessagesFile: "compiler:Languages\Armenian.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "bulgarian"; MessagesFile: "compiler:Languages\Bulgarian.isl"
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "corsican"; MessagesFile: "compiler:Languages\Corsican.isl"
Name: "czech"; MessagesFile: "compiler:Languages\Czech.isl"
Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"
Name: "icelandic"; MessagesFile: "compiler:Languages\Icelandic.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "slovak"; MessagesFile: "compiler:Languages\Slovak.isl"
Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_decimal.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_elementtree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_multiprocessing.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_queue.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\_tkinter.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\base_library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\fbx.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\fbxsip.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\libcrypto-1_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\libopenblas.XWYDX2IKJW2NMTWSFYNGFUWKQU3LYTCZ.gfortran-win_amd64.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\libssl-1_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\MSVCP140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\python37.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\tcl86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\tk86t.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\VCRUNTIME140_1.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\altgraph-0.17.2.dist-info\*"; DestDir: "{app}\altgraph-0.17.2.dist-info"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\documentation\*"; DestDir: "{app}\documentation"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\imageio\*"; DestDir: "{app}\imageio"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\imageio_ffmpeg\*"; DestDir: "{app}\imageio_ffmpeg"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\numpy\*"; DestDir: "{app}\numpy"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\PIL\*"; DestDir: "{app}\PIL"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\pandas\*"; DestDir: "{app}\pandas"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\pyinstaller-4.10.dist-info\*"; DestDir: "{app}\pyinstaller-4.10.dist-info"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\setuptools-47.1.0.dist-info\*"; DestDir: "{app}\setuptools-47.1.0.dist-info"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\tcl\*"; DestDir: "{app}\tcl"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\tcl8\*"; DestDir: "{app}\tcl8"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Yassine\Documents\upwork\tbx2\TBXSOURCE\TBXSOURCE\dist\main\tk\*"; DestDir: "{app}\tk"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

