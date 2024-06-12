@echo off
chcp 65001
set currentTime=%TIME%
set currentHour=%currentTime:~0,2%
set currentMinute=%currentTime:~3,2%

set thresholdHour=7
set thresholdMinute=30

@REM 今日の日付け取得
for /f "delims=" %%a in ('wmic os get LocalDateTime ^| find "."') do set datetime=%%a
set "today=%datetime:~0,8%"

set path1=C:\Users\RP00056\monitor_order_delay\data\result_%today%.csv
set "pathA=C:\Winactor\本番\管理課\工務\未受入れ未検収進捗\DL未検収データ\"
set "pathB=未検収データ"
set "path2=%pathA%%today%%pathB%.csv"

echo %path1%
echo %path2%

if not exist %path2% (
  start /wait cmd /c C:\Winactor\本番\管理課\工務\未受入れ未検収進捗\未受入未検収進捗_morning_first_data.vbs
  call :checkErrorLevel %errorlevel%
)
timeout /t 120
if not exist %path1% (
  start /wait cmd /c C:\Users\RP00056\monitor_order_delay\createEntireDataOfTheDay.bat
  call :checkErrorLevel %errorlevel%
)


cd C:\Users\RP00056\monitor_order_delay\source_prod
streamlit run main.py

:checkErrorLevel
if %1 neq 0 (
    echo Error occurred in the previous batch file. Exit code: %1
    rem Handle error as needed
    exit /b %1
)
exit /b
