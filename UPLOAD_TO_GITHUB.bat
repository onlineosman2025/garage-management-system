@echo off
echo ═══════════════════════════════════════════════════════════════════
echo           UPLOAD TO GITHUB - AUTOMATED SCRIPT
echo ═══════════════════════════════════════════════════════════════════
echo.

REM Check if git user is configured
git config user.name >nul 2>&1
if errorlevel 1 (
    echo ❌ Git user not configured!
    echo.
    echo Please run these commands first:
    echo   git config --global user.name "Your Name"
    echo   git config --global user.email "your@email.com"
    echo.
    pause
    exit /b 1
)

echo ✅ Git user configured
echo.

REM Commit changes
echo 📝 Committing changes...
git commit -m "Add all project files"
if errorlevel 1 (
    echo ⚠️  Commit failed or nothing to commit
    echo.
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo Now you need to:
echo.
echo 1. Create GitHub repository at: https://github.com/new
echo    Name: garage-management-system
echo    Don't add README, .gitignore, or license
echo.
echo 2. Copy your repository URL (looks like):
echo    https://github.com/YOUR_USERNAME/garage-management-system.git
echo.
echo 3. Run these commands:
echo.
echo    git remote add origin YOUR_REPO_URL
echo    git branch -M main
echo    git push -u origin main
echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
