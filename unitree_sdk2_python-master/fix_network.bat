@echo off
:: Request Admin Privileges
NET FILE 1>NUL 2>NUL
if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)
ECHO Set UAC = CreateObject^("Shell.Application"^) > "%temp%\OEgetPrivileges.vbs"
ECHO UAC.ShellExecute "%~s0", "ELEV", "", "runas", 1 >> "%temp%\OEgetPrivileges.vbs"
"%temp%\OEgetPrivileges.vbs"
exit /B

:gotPrivileges
echo Dang thiet lap Interface Metric cho Ethernet 2...
powershell -Command "Set-NetIPInterface -InterfaceAlias 'Ethernet 2' -InterfaceMetric 1"
echo Da thiet lap xong! Vui long tat bang nay.
pause
