WINACTOR_PATH="""C:\Program Files (x86)\WinActor7\WinActor7.exe"""
WINACTOR_OPT="-f ""C:\Winactor\本番\管理課\工務\未受入れ未検収進捗\未受入未検収進捗.ums7"" -r -e"
Set objShell = WScript.CreateObject("WScript.Shell")
Set objExec = objShell.Exec(WINACTOR_PATH & " " & WINACTOR_OPT)

