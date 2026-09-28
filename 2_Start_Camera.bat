@echo off
title DJI Action 5 to Mindstorms camera
cd /d "%~dp0"
set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"

if not exist "mediamtx\mediamtx.exe" (
    echo MediaMTX is missing. Run 1_Install_First_Time.bat first.
    pause
    exit /b 1
)

tasklist /fi "imagename eq obs64.exe" | find /i "obs64.exe" >nul
if not errorlevel 1 (
    echo NOTE: OBS Studio is open. If OBS's own "Start Virtual Camera" is on,
    echo       this will not work - close OBS first.
    echo.
)

tasklist /fi "imagename eq mediamtx.exe" | find /i "mediamtx.exe" >nul
if errorlevel 1 (
    echo Starting MediaMTX video server - minimized window, leave it open...
    start "MediaMTX - leave open" /min /d "%~dp0mediamtx" "%~dp0mediamtx\mediamtx.exe"
) else (
    echo MediaMTX video server is already running.
)
echo.

"%PY%" -u stream_to_vcam.py

echo.
echo Camera stopped. Run 3_Stop_Camera.bat to also stop the MediaMTX server.
pause
