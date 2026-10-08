@echo off
chcp 65001 >nul
title LẤY MÃ BẢO MẬT ROBOT TỪ TÀI KHOẢN UNITREE CLOUD
color 0E

if not exist "venv\Scripts\python.exe" (
    color 0C
    echo ❌ Chưa tìm thấy môi trường venv!
    echo Vui lòng chạy file [1_CAI_DAT_MAY_MOI.bat] trước để cài đặt thư viện.
    echo.
    pause
    exit /b
)

.\venv\Scripts\python.exe lay_key_robot.py
