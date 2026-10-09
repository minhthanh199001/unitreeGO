@echo off
chcp 65001 >nul
title LEHOANG ROBOTICS - KHỞI CHẠY MÁY CHỦ ROBOT
color 0B

:: Đảm bảo luôn chạy tại đúng thư mục chứa file .bat
cd /d "%~dp0"

echo =======================================================================
echo          LEHOANG ROBOTICS - KHỞI ĐỘNG HỆ THỐNG ĐIỀU KHIỂN ROBOT
echo =======================================================================
echo.

if not exist "venv\Scripts\python.exe" (
    color 0C
    echo ❌ Chưa tìm thấy môi trường venv!
    echo Vui lòng chạy file [1_CAI_DAT_MAY_MOI.bat] trước để hệ thống tự cài đặt.
    echo.
    pause
    exit /b
)

if not exist "cert.pem" (
    echo Đang tạo chứng chỉ SSL/HTTPS bảo mật...
    .\venv\Scripts\python.exe generate_cert.py
)

echo 🚀 Đang khởi chạy máy chủ HTTPS tại cổng 8080...
echo 🌐 Địa chỉ trên máy tính này: https://localhost:8080
echo 📱 Địa chỉ trên điện thoại   : https://192.168.0.60:8080
echo.
echo (Nhấn Ctrl + C trong cửa sổ này nếu bạn muốn dừng máy chủ)
echo =======================================================================
echo.

:: Tự động mở trình duyệt sau 1.5 giây
start "" https://localhost:8080

:: Chạy server FastAPI HTTPS
.\venv\Scripts\python.exe -u app.py

pause
