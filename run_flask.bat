@echo off
REM ------------------------------
REM Остановка старого сервера Flask
REM ------------------------------
if exist "flask.pid" (
    for /F %%i in (flask.pid) do (
        tasklist /FI "PID eq %%i" | find "%%i" >nul && taskkill /PID %%i /F || echo Process %%i not running
    )
    del "flask.pid"
)

REM ------------------------------
REM Запуск Flask в фоне
REM ------------------------------
cd /d %~dp0

REM Запускаем Flask на 0.0.0.0:5000 и сохраняем PID
start /B "" python -m flask run --host=0.0.0.0 --port=5000 1>flask.log 2>&1

REM Сохраняем PID последнего запущенного процесса в flask.pid
for /f "tokens=2 delims=," %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH') do (
    echo %%~a > flask.pid
    goto :break
)
:break

echo Flask server started. Log: flask.log
