@echo off
setlocal

set PYTHON_SCRIPT="C:\Apps\media-docker-credentials\start_cron_docker.py"
set VENV_ACTIVATE="C:\Venvs\media-docker-credentials\Scripts\activate.bat"
set LOGFILE="%LOCALAPPDATA%\media-docker-credentials\logs\cron_log.txt"

if not exist "%LOCALAPPDATA%\media-docker-credentials\logs" (
    mkdir "%LOCALAPPDATA%\media-docker-credentials\logs"
)

echo =========================== >> %LOGFILE%
echo START TIME: %date% %time% >> %LOGFILE%
echo USERNAME: %USERNAME% >> %LOGFILE%
echo --------------------------- >> %LOGFILE%

REM Wait for 1 minute
timeout /t 60 /nobreak

call %VENV_ACTIVATE%

python %PYTHON_SCRIPT% >> %LOGFILE% 2>&1

REM Log completion
echo --------------------------- >> %LOGFILE%
echo END TIME: %date% %time% >> %LOGFILE%
echo =========================== >> %LOGFILE%
echo. >> %LOGFILE%

endlocal
