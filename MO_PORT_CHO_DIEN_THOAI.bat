@echo off
chcp 65001 > nul
:: Yeu cau quyen Administrator de mo Firewall
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)
ECHO Set UAC = CreateObject^("Shell.Application"^) > "%temp%\OEgetPrivileges.vbs"
ECHO UAC.ShellExecute "%~s0", "ELEV", "", "runas", 1 >> "%temp%\OEgetPrivileges.vbs"
"%temp%\OEgetPrivileges.vbs"
exit /B

:gotPrivileges
title MO PORT 8080 CHO DIEN THOAI TRUY CAP
echo =====================================================================
echo    DANG MO KHOA FIREWALL CONG 8080 DE DIEN THOAI KET NOI
echo =====================================================================
echo.
netsh advfirewall firewall delete rule name="Unitree WebApp Port 8080" >nul 2>&1
netsh advfirewall firewall add rule name="Unitree WebApp Port 8080" dir=in action=allow protocol=TCP localport=8080
echo.
echo [THANH CONG] Da mo cong 8080 tren Windows Firewall!
echo Dien thoai trong cung mang Wi-Fi co the ket noi vao dia chi WebApp.
echo.
pause
