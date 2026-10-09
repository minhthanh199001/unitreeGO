@echo off
chcp 65001 >nul
title DỪNG MÁY CHỦ LEHOANG ROBOTICS
color 0C

echo =======================================================================
echo          LEHOANG ROBOTICS - DỪNG MÁY CHỦ ROBOT ĐANG CHẠY ẨN
echo =======================================================================
echo.

powershell -Command "Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*unitreego*' } | Stop-Process -Force"

echo ✅ Đã dừng toàn bộ máy chủ robot đang chạy ẩn!
echo.
timeout /t 3
