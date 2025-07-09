@echo off
echo Installing BuraqManager...

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as administrator - proceeding with installation
) else (
    echo Please run this script as administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Create installation directory
set "INSTALL_DIR=%PROGRAMFILES%\BuraqManager"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying files...
copy "BuraqManager.exe" "%INSTALL_DIR%\"
copy "buraqmanager.db" "%INSTALL_DIR%\"

REM Create Start Menu shortcut
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\BuraqManager"
if not exist "%START_MENU%" mkdir "%START_MENU%"

echo Creating shortcuts...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\BuraqManager.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\BuraqManager.exe'; $Shortcut.Save()"

REM Create Desktop shortcut
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\BuraqManager.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\BuraqManager.exe'; $Shortcut.Save()"

REM Add to registry for uninstall
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BuraqManager" /v "DisplayName" /t REG_SZ /d "BuraqManager" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BuraqManager" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f

REM Create uninstall script
echo @echo off > "%INSTALL_DIR%\uninstall.bat"
echo echo Uninstalling BuraqManager... >> "%INSTALL_DIR%\uninstall.bat"
echo del "%START_MENU%\BuraqManager.lnk" >> "%INSTALL_DIR%\uninstall.bat"
echo rmdir "%START_MENU%" >> "%INSTALL_DIR%\uninstall.bat"
echo del "%USERPROFILE%\Desktop\BuraqManager.lnk" >> "%INSTALL_DIR%\uninstall.bat"
echo reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\BuraqManager" /f >> "%INSTALL_DIR%\uninstall.bat"
echo rmdir /s /q "%INSTALL_DIR%" >> "%INSTALL_DIR%\uninstall.bat"
echo echo Uninstallation complete. >> "%INSTALL_DIR%\uninstall.bat"
echo pause >> "%INSTALL_DIR%\uninstall.bat"

echo.
echo Installation complete!
echo BuraqManager has been installed to: %INSTALL_DIR%
echo Shortcuts have been created on the desktop and start menu.
echo.
pause 