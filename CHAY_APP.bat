@echo off
chcp 65001 > nul
title UNITREE GO2 CONTROLLER

cd /d "%~dp0unitree_sdk2_python-master"

if exist ".\venv\Scripts\pythonw.exe" (
    start "" ".\venv\Scripts\pythonw.exe" "app_launcher.py"
) else (
    echo [LOI] Khong tim thay moi truong Python venv!
    echo Dang thu chay bang python he thong...
    start "" pythonw "app_launcher.py"
)

exit
