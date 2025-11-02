@echo off
title PWA Icon Generator
color 0A

echo.
echo ==========================================
echo    PWA ICON GENERATOR
echo    Garage Management System
echo ==========================================
echo.

echo Choose your method:
echo.
echo [1] Open HTML Icon Generator (Recommended)
echo [2] Run Python Icon Generator
echo [3] Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Opening HTML Icon Generator...
    echo.
    start http://localhost:3000/generate-icons.html
    echo.
    echo Instructions:
    echo 1. Click "Download All Icons" button
    echo 2. All icons will download automatically
    echo 3. Icons are saved in your Downloads folder
    echo 4. Move them to the /icons folder
    echo.
    pause
) else if "%choice%"=="2" (
    echo.
    echo Checking for Pillow...
    python -c "import PIL" 2>nul
    if errorlevel 1 (
        echo.
        echo [ERROR] Pillow not installed!
        echo.
        echo Installing Pillow...
        pip install Pillow
        echo.
    )
    echo.
    echo Generating icons...
    python generate_icons.py
    echo.
    pause
) else (
    echo.
    echo Goodbye!
    timeout /t 2 >nul
    exit
)
