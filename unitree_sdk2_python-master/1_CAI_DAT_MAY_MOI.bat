@echo off
chcp 65001 >nul
title CÀI ĐẶT HỆ THỐNG ĐIỀU KHIỂN UNITREE GO2 (LEHOANG ROBOTICS)
color 0B

echo =======================================================================
echo          LEHOANG ROBOTICS - CÀI ĐẶT TỰ ĐỘNG CHO MÁY TÍNH MỚI
echo =======================================================================
echo.

:: 1. Kiểm tra Python
echo [1/5] Đang kiểm tra phiên bản Python trên máy tính...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ❌ CHƯA CÀI ĐẶT PYTHON!
    echo Vui lòng cài đặt Python (Khuyên dùng Python 3.10, 3.11 hoặc 3.12).
    echo Tải tại: https://www.python.org/downloads/
    echo ⚠️ LƯU Ý KHI CÀI: Tích chọn ô [Add python.exe to PATH]!
    echo.
    pause
    exit /b
)
python --version

:: 2. Khởi tạo Virtual Environment
echo.
echo [2/5] Đang thiết lập môi trường ảo độc lập (venv)...
if not exist "venv\" (
    python -m venv venv
    echo -> Đã tạo mới thư mục venv thành công!
) else (
    echo -> Môi trường ảo venv đã có sẵn.
)

:: 3. Nâng cấp PIP và cài đặt thư viện
echo.
echo [3/5] Đang cài đặt các thư viện cần thiết từ requirements.txt...
echo (Quá trình này có thể mất 1-3 phút tùy tốc độ mạng, vui lòng đợi...)
.\venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.\venv\Scripts\pip.exe install -r requirements.txt

:: 4. Cài đặt SDK Unitree nội bộ
echo.
echo [4/5] Đang cài đặt gói SDK điều khiển Unitree (unitree_sdk2py)...
.\venv\Scripts\pip.exe install -e .

:: 5. Tạo chứng chỉ bảo mật SSL/HTTPS
echo.
echo [5/5] Đang tạo chứng chỉ bảo mật HTTPS cục bộ (cert.pem & key.pem)...
if not exist "cert.pem" (
    .\venv\Scripts\python.exe generate_cert.py
) else (
    echo -> Chứng chỉ bảo mật cert.pem & key.pem đã sẵn sàng!
)

color 0A
echo.
echo =======================================================================
echo ✅ CÀI ĐẶT HOÀN TẤT 100%! HỆ THỐNG ĐÃ SẴN SÀNG SỬ DỤNG.
echo.
echo 👉 BƯỚC TIẾP THEO:
echo   1. Nếu là robot của bạn: Nhấp đúp vào file [2_CHAY_ROBOT.bat] để bắt đầu.
echo   2. Nếu khách dùng tài khoản Unitree khác: Chạy file [3_LAY_KEY_TAI_KHOAN_MOI.bat]
echo      để tự động lấy mã bảo mật AES Key từ tài khoản khách!
echo =======================================================================
echo.
pause
