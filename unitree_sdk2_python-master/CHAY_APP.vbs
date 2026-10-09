' =====================================================================
' LEHOANG ROBOTICS - KHỞI CHẠY ẨN TRÊN DESKTOP KHÔNG HIỆN MÀN HÌNH ĐEN
' =====================================================================
Option Explicit

Dim WshShell, fso, scriptDir, targetDir, pythonExe, appScript, batFile

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Xác định thư mục chứa mã nguồn ứng dụng
If fso.FileExists(scriptDir & "\app.py") Then
    targetDir = scriptDir
ElseIf fso.FileExists("D:\THANH\unitreego\unitree_sdk2_python-master\app.py") Then
    targetDir = "D:\THANH\unitreego\unitree_sdk2_python-master"
Else
    MsgBox "Không tìm thấy thư mục chứa file app.py!", vbCritical, "LEHOANG ROBOTICS - Lỗi"
    WScript.Quit
End If

pythonExe = targetDir & "\venv\Scripts\python.exe"
appScript = targetDir & "\app.py"
batFile = targetDir & "\CHAY_APP.bat"

' Kiểm tra xem môi trường ảo venv đã tồn tại chưa
If Not fso.FileExists(pythonExe) Then
    MsgBox "Chưa tìm thấy môi trường Python venv! Vui lòng chạy file 1_CAI_DAT_MAY_MOI.bat trước.", vbExclamation, "LEHOANG ROBOTICS"
    WScript.Quit
End If

' Đổi thư mục làm việc về đúng thư mục ứng dụng
WshShell.CurrentDirectory = targetDir

' Khởi chạy server FastAPI trong nền ẩn hoàn toàn (Cửa sổ ẩn: 0)
WshShell.Run """" & pythonExe & """ -u """ & appScript & """", 0, False

' Đợi 2 giây để server hoàn tất khởi động cổng 8080
WScript.Sleep 2000

' Tự động mở trình duyệt web tới giao diện điều khiển
WshShell.Run "https://localhost:8080"
