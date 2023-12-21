@echo off

REM Get the current IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4 Address"') do set "IP=%%a"

@echo off
setlocal enabledelayedexpansion
set "URL=http://%IP%:8000/bill"
start chrome !URL!
call .venv\Scripts\activate
waitress-serve --port=8000 Exellent.wsgi:application