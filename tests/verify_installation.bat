@echo off
echo Activating virtual environment...
call .venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo Virtual environment not found or activation failed.
    echo Proceeding without virtual environment...
    echo.
)
echo.
echo Verifying component installation...
python verify_installation.py
echo.
echo Press any key to exit...
pause >nul