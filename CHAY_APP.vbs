Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

pythonwPath = currentDir & "\unitree_sdk2_python-master\venv\Scripts\pythonw.exe"
launcherPath = currentDir & "\unitree_sdk2_python-master\app_launcher.py"

If fso.FileExists(pythonwPath) Then
    WshShell.CurrentDirectory = currentDir & "\unitree_sdk2_python-master"
    WshShell.Run """" & pythonwPath & """ """ & launcherPath & """", 0, False
Else
    WshShell.Run """" & currentDir & "\CHAY_APP.bat""", 0, False
End If
