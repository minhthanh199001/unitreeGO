@echo off
chcp 65001 > nul
title DIEU KHIEN DONG BO 2 ROBOT UNITREE GO2
echo =====================================================================
echo    HE THONG DIEU KHIEN DONG BO 2 ROBOT UNITREE GO2 - LAN ROUTER
echo =====================================================================
echo.
echo Robot 1: IP 192.168.0.41 (AES Key Enabled)
echo Robot 2: IP 192.168.0.75 (Go2 Edu)
echo.
echo Luu y: Dam bao da TAT ung dung Unitree tren dien thoai truoc khi chay!
echo.
echo Dang khoi dong Web Server tai http://localhost:8080 ...
echo Ban co the mo trinh duyet vao dia chi tren de dieu khien.
echo.
cd /d "%~dp0"
.\venv\Scripts\python.exe -u app.py
pause
