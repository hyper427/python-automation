@echo off
setlocal

set "PROJECT_DIR=C:\Users\user\Desktop\python-automation"
set "LOG_FILE=%PROJECT_DIR%\log_market_report.txt"

cd /d "%PROJECT_DIR%"

echo ============================================== >> "%LOG_FILE%"
echo [%date% %time%] market report start >> "%LOG_FILE%"

call "%PROJECT_DIR%\.venv\Scripts\activate.bat"

python "%PROJECT_DIR%\market_report.py" >> "%LOG_FILE%" 2>&1

echo [%date% %time%] git add/commit/push >> "%LOG_FILE%"

git add market_report_*.md market_report_*.html index.html >> "%LOG_FILE%" 2>&1
git commit -m "Update market report %date% %time%" >> "%LOG_FILE%" 2>&1
git push >> "%LOG_FILE%" 2>&1

echo [%date% %time%] market report end >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

endlocal
