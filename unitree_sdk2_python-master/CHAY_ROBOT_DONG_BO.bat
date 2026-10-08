@echo off
chcp 65001 > nul
title DIEU KHIEN DONG BO ROBOT UNITREE GO2
echo =====================================================================
echo    HE THONG DIEU KHIEN DONG BO ROBOT UNITREE GO2 - LAN ROUTER
echo =====================================================================
echo.
echo Luu y: Dam bao da TAT ung dung Unitree tren dien thoai truoc khi chay!
echo.
echo Dang khoi dong Web Server tai http://localhost:8080 ...
echo Trinh duyet web se tu dong duoc mo sau 2 giay...
echo.
cd /d "%~dp0"
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8080"
.\venv\Scripts\python.exe -u app.py
pause
