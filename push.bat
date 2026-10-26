@echo off
cd /d "%~dp0"
echo ========================================================
echo    AgroScan AI - Automatic Git Push to GitHub
echo ========================================================
echo.

echo 1. Staging changes...
git add .
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Git add failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo 2. Committing changes...
git commit -m "feat: multi-species plant AI identification, self-credential auth, and multi-device compatibility"
if %ERRORLEVEL% neq 0 (
    echo [NOTE] No new changes to commit or commit completed.
)

echo.
echo 3. Pushing to origin main...
git push origin main
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Git push failed. Please check your internet or GitHub credentials.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================================
echo [SUCCESS] All updates successfully pushed to GitHub!
echo Vercel and Render will now deploy the updates automatically.
echo ========================================================
echo.
pause
