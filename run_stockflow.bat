@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations organizations accounts inventory
if errorlevel 1 goto error
python manage.py migrate
if errorlevel 1 goto error
echo.
echo StockFlow is ready. Open http://127.0.0.1:8000/
python manage.py runserver
goto end
:error
echo.
echo Setup failed. Read the error above and check the README.
pause
:end
endlocal
