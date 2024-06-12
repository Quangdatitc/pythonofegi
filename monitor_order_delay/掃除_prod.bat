 
@echo off
@REM ------------------------------未検収データ----------------------------------------
@REM 変数をconstタイプから外す
setlocal enabledelayedexpansion

@REM 日本文字を打てるようにする
chcp 65001 > nul 

@REM 今日の日付け取得
for /f "delims=" %%a in ('wmic os get LocalDateTime ^| find "."') do set datetime=%%a
set "today=!datetime:~0,8!"

@REM 未検収バックアップフォルダ
set "targetFolderUninspected=C:\Winactor\本番\管理課\工務\未受入れ未検収進捗\DL未検収データ\backup未検収データ"
@REM 未検収ファイルあるフォルダ
set "sourceFolderUninspected=C:\Winactor\本番\管理課\工務\未受入れ未検収進捗\DL未検収データ"

@REM バックアップフォルダがなければ作成する
if not exist "%targetFolderUninspected%" mkdir "%targetFolderUninspected%"

@REM 今日の日付ついてるまた未検収データ.csvのみ残して他はバックアップフォルダへ移動
for /r "%sourceFolderUninspected%" %%F in (*.csv) do (
    @REM ファイルの拡張を捨てて名前だけ取得
    set "filename=%%~nF"
    @REM 最初の８桁を取得
    set "filedate=!filename:~0,8!"

    if not "!filedate!" equ "!today!" if not "%%~nF" equ "未検収データ" (
        move "%%F" "%targetFolderUninspected%"
    )
)

echo 未検収移動完了

@REM ------------------------------検収実績----------------------------------------

@REM 検収実績バックアップフォルダ
set "targetFolderInspected=C:\Winactor\本番\管理課\工務\報告履歴照会DL\報告履歴照会DLデータ\backup検収実績"
@REM 検収実績フォルダ
set "sourceFolderInspected=C:\Winactor\本番\管理課\工務\報告履歴照会DL\報告履歴照会DLデータ"

if not exist "%targetFolderInspected%" mkdir "%targetFolderInspected%"

@REM 今日の日付ついてる検収実績.csvのみ残して他はバックアップフォルダへ移動
for /r "%sourceFolderInspected%" %%F in (*.csv) do (
    @REM ファイルの拡張を捨てて名前だけ取得
    set "filename=%%~nF"
    @REM 最初の８桁を取得
    set "filedate=!filename:~0,8!"

    if not "!filedate!" equ "!today!" if not "%%~nF" equ "検収実績" (
        move "%%F" "%targetFolderInspected%"
    )
)
echo 検収実績完了


@REM ------------------------------Log----------------------------------------
C:\Users\CZ71947\TestBranch\未受入れ未検収進捗\BATCHTEST\Log

@REM Logバックアップフォルダ

set "targetFolderLog=C:\Users\RP00056\monitor_order_delay\Log\backupLog"
@REM Logフォルダ
set "sourceFolderLog=C:\Users\RP00056\monitor_order_delay\Log"

if not exist "%targetFolderLog%" mkdir "%targetFolderLog%"

@REM 今日の日付ついてるstreamline_log_$todayのみ残して他はバックアップフォルダへ移動
for /r "%sourceFolderLog%" %%F in (*.log) do (
    @REM ファイルの拡張を捨てて名前だけ取得
    set "filename=%%~nF"
    @REM 最後の８桁を取得
    set "filedate=!filename:~-8!"

    if not "!filedate!" equ "!today!" (
        move "%%F" "%targetFolderLog%"
    )
)
echo 検収実績完了


@REM ------------------------------Result当日EntireData----------------------------------------
C:\Users\CZ71947\TestBranch\未受入れ未検収進捗\BATCHTEST\Log

@REM Resultバックアップフォルダ

set "targetFolderData=C:\Users\RP00056\monitor_order_delay\data\backupResult"
@REM Dataフォルダ
set "sourceFolderData=C:\Users\RP00056\monitor_order_delay\data"

if not exist "%targetFolderData%" mkdir "%targetFolderData%"

@REM 今日の日付ついてるresult_$todayのみ残して他はバックアップフォルダへ移動
for /r "%sourceFolderData%" %%F in (result*.csv) do (
    @REM ファイルの拡張を捨てて名前だけ取得
    set "filename=%%~nF"
    @REM 最初の８桁を取得
    set "filedate=!filename:~-8!"

    if not "!filedate!" equ "!today!" if not "%%~nF" equ "result" (
        move "%%F" "%targetFolderData%"
    )
)
echo 検収実績完了



@REM ------------------------------master_extract当日----------------------------------------
C:\Users\CZ71947\TestBranch\未受入れ未検収進捗\BATCHTEST\Log


@REM 日付けはちょっと違う YYYY-MM-DD
for /f "delims=" %%a in ('wmic os get LocalDateTime ^| find "."') do set datetime=%%a
set "today=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!"


@REM master当日分バックアップフォルダ

set "targetFolderMasterExtract=C:\Users\RP00056\monitor_order_delay\data\backupMasterExtract"
@REM Dataフォルダ
set "sourceFolderData=C:\Users\RP00056\monitor_order_delay\data"

if not exist "%targetFolderMasterExtract%" mkdir "%targetFolderMasterExtract%"

@REM 今日の日付ついてるresult_$todayのみ残して他はバックアップフォルダへ移動
for /r "%sourceFolderData%" %%F in (master_extract*.xlsx) do (
    @REM ファイルの拡張を捨てて名前だけ取得
    set "filename=%%~nF"
    @REM 最初の８桁を取得
    set "filedate=!filename:~-10!"

    if not "!filedate!" equ "!today!" if not "%%~nF" equ "result" (
        move "%%F" "%targetFolderMasterExtract%"
    )
)
echo master_extract