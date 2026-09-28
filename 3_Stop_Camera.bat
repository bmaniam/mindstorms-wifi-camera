@echo off
title Stop DJI Mindstorms Camera
echo Stopping camera...
taskkill /im mediamtx.exe /f >nul 2>nul && echo  - MediaMTX video server stopped
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -like '*stream_to_vcam.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; ' - camera script stopped' }"
echo Done.
timeout /t 3 >nul
