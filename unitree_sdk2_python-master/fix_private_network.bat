@echo off
:: Request Admin
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)
ECHO Set UAC = CreateObject^("Shell.Application"^) > "%temp%\OEgetPrivileges.vbs"
ECHO UAC.ShellExecute "%~s0", "ELEV", "", "runas", 1 >> "%temp%\OEgetPrivileges.vbs"
"%temp%\OEgetPrivileges.vbs"
exit /B

:gotPrivileges
echo Dang chuyen mang LAN sang Private Network de mo khoa DDS...
powershell -Command "Set-NetConnectionProfile -InterfaceAlias 'Ethernet 2' -NetworkCategory Private"
echo Da thiet lap xong! Vui long tat bang nay.
pause
