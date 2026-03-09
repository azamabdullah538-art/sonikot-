ter name="content">@echo off
echo ============================================
echo Pushing to GitHub - Sonikot Welfare Organization
echo ============================================

cd /d "d:\sonikot welfear organization"

echo.
echo Checking git installation...
git --version
if errorlevel 1 (
    echo Git is not installed or not in PATH
    echo Please restart your terminal and try again
    pause
    exit /b 1
)

echo.
echo Initializing git repository...
git init

echo.
echo Adding files...
git add .

echo.
echo Committing changes...
git commit -m "Fixed contact form messages, home page image, and programs with icons"

echo.
echo Adding remote origin...
git remote add origin https://github.com/azamabdullah538-art/sonikot-.git

echo.
echo Pushing to GitHub...
git push -u origin main

echo.
echo ============================================
echo Done! Check your GitHub repository.
echo ============================================
pause
