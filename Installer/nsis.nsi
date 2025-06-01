!include "MUI2.nsh"
Name "Meijo Print Installer"
BrandingText "2025 @ugokitakunai:github"
OutFile "Installer.exe"
InstallDir "$LOCALAPPDATA\MeijoPrintService"

!insertmacro MUI_PAGE_INSTFILES

Section
  SetOutPath "$TEMP\MPS_Setup"
  File VC_redist.x64.exe
  ExecWait '"$TEMP\MPS_Setup\VC_redist.x64.exe" /quiet /norestart'
  File "7z.exe"
  File "7z.dll"
  StrCpy $0 "$TEMP\MPS_Setup\gsinstaller.exe"
  StrCpy $1 "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10051/gs10051w64.exe"
  
inetc::get /popup "" $1 $0
  Pop $2
  DetailPrint "Download result: $2"
  StrCmp $2 "OK" +2
    Abort "Download failed."

ExecWait '"$TEMP\MPS_Setup\7z.exe" x "$TEMP\MPS_Setup\gsinstaller.exe" -o"$TEMP\MPS_Setup" -y'

CreateDirectory "$INSTDIR\bin"
CopyFiles "$TEMP\MPS_Setup\bin\*.*" "$INSTDIR\bin"

CreateDirectory "$INSTDIR\Resource"
CopyFiles "$TEMP\MPS_Setup\Resource\*.*" "$INSTDIR\Resource"

CreateDirectory "$INSTDIR\iccprofiles"
CopyFiles "$TEMP\MPS_Setup\iccprofiles\*.*" "$INSTDIR\iccprofiles"

CreateDirectory "$INSTDIR\lib"
CopyFiles "$TEMP\MPS_Setup\lib\*.*" "$INSTDIR\lib"
  SetOutPath "$INSTDIR"

File "python.zip"
ExecWait '"$TEMP\MPS_Setup\7z.exe" x "$INSTDIR\python.zip" -o"$INSTDIR"' 

  File "..\*.py"
  File "..\requirements.txt"
nsExec::ExecToLog '"$INSTDIR\python\python.exe" $INSTDIR\python\get-pip.py'
  nsExec::ExecToLog '"$INSTDIR\python\python.exe" -m pip install -r requirements.txt'
  nsExec::ExecToLog '"$INSTDIR\python\python.exe" $INSTDIR\create_secret.py'
  nsExec::ExecToLog '"$INSTDIR\python\python.exe" "$INSTDIR\install_printer.py"'
  
  ReadRegStr $0 HKCU "Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" "Startup"
  CreateShortCut "$0\MeijoPrintServer.lnk" "$INSTDIR\python\Scripts\pythonw.exe" '"$INSTDIR\print_server.py"' "" 0 SW_SHOWNORMAL

  Exec '"$INSTDIR\python\pythonw.exe" "$INSTDIR\print_server.py"'
SectionEnd
