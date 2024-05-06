@echo off

set REPO_DIR=%~dp0
cd /D %REPO_DIR%

echo Checking if Git is installed...
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed.
    echo Attempting to download and install Git...
    powershell -command "try { Invoke-WebRequest 'https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/Git-2.45.0-64-bit.exe' -OutFile '%temp%\GitInstaller.exe'; Start-Process '%temp%\GitInstaller.exe' -ArgumentList '/VERYSILENT /NORESTART' -Wait; Remove-Item '%temp%\GitInstaller.exe' -Force; } catch { echo 'Failed to download or install Git. Please check your internet connection and try again.'; ; exit }"
    echo Git has been installed successfully.
    echo Please relaunch the script to complete.
    pause
    exit
)

rem Initialize Git repository if not already a repo
if not exist .git (
    echo Initializing Git repository...
    git init
    git remote add origin "https://github.com/MrDOSmile/DOSaveGuardian.git"
    echo Repository initialized and remote set.
)

echo Fetching updates from GitHub...
git fetch --all --verbose
if %errorlevel% neq 0 (
    echo Failed to fetch updates.
    goto check_python
)

echo Resetting local files to match remote main branch...
git reset --hard origin/main
if %errorlevel% neq 0 (
    echo Failed to reset files.
    goto check_python
)

echo Repository setup complete. Local directory is now synchronized with remote.

:check_python
echo Checking Python and required packages...
python -m pip show ursina > nul 2>&1
if %errorlevel% neq 0 (
    echo Ursina is not installed. Installing required Python packages...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install Python packages. Please check your Python installation.
        exit
    )
    echo Python packages installed successfully.
)


