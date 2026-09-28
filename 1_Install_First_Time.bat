@echo off
title First-time setup - DJI Mindstorms Camera
cd /d "%~dp0"
set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"

if not exist "%PY%" (
    echo Installing Python 3.12...
    winget install -e --id Python.Python.3.12 --scope user --silent --accept-package-agreements --accept-source-agreements
)
if not exist "%PY%" (
    echo.
    echo Python install failed. Install Python 3.12 from https://www.python.org/downloads/
    echo then run this file again.
    pause
    exit /b 1
)

echo.
echo Installing Python packages...
"%PY%" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo.
    echo Package install failed. Check the internet connection and run this file again.
    pause
    exit /b 1
)

if not exist "mediamtx\mediamtx.exe" (
    echo.
    echo Downloading MediaMTX video server from github.com/bluenviron/mediamtx ...
    powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -UseBasicParsing -Uri 'https://github.com/bluenviron/mediamtx/releases/download/v1.21.0/mediamtx_v1.21.0_windows_amd64.zip' -OutFile 'mediamtx.zip'; Expand-Archive -Force 'mediamtx.zip' 'mediamtx'; Remove-Item 'mediamtx.zip'"
)
if not exist "mediamtx\mediamtx.exe" (
    echo.
    echo MediaMTX download failed. Download mediamtx_v1.21.0_windows_amd64.zip from
    echo https://github.com/bluenviron/mediamtx/releases and unzip it into a folder
    echo named "mediamtx" next to this file, then run this file again.
    pause
    exit /b 1
)

if not exist "%ProgramFiles%\obs-studio\data\obs-plugins\win-dshow\obs-virtualcam-module64.dll" (
    echo.
    echo OBS Studio is not installed. It provides the "OBS Virtual Camera" device.
    echo Installing OBS Studio - click Yes if Windows asks for permission...
    winget install -e --id OBSProject.OBSStudio --accept-package-agreements --accept-source-agreements
)

echo.
echo ============================================================
echo  Setup finished. From now on, just double-click
echo  2_Start_Camera.bat
echo ============================================================
pause
