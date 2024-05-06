@echo off

rem Set the directory where your repository is located
set REPO_DIR=%~dp0
echo Current Repository Directory: %REPO_DIR%


rem Change to the repository directory
cd /D %REPO_DIR%

rem Check if Git is installed
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed.

    echo Downloading Git...
    powershell -command "& { (New-Object Net.WebClient).DownloadFile('https://github.com/git-for-windows/git/releases/latest/download/Git-x64.exe', '%temp%\GitInstaller.exe') }"
    echo Installing Git...
    start /wait %temp%\GitInstaller.exe /VERYSILENT /NORESTART
    echo Git installed successfully.

)

rem Initialize Git repository if not already a repo
if not exist .git (
    echo Initializing Git repository...
    git init
    git remote add origin https://github.com/MrDOSmile/DOSaveGuardian.git
    echo Repository initialized and remote set.

)

rem Check for internet connectivity before proceeding
ping -n 1 google.com > nul 2>&1
if %errorlevel% neq 0 (
    echo No internet connection detected. Please check your network settings.

    goto run_script
)

rem Fetching and resetting the repository to match the remote main branch
echo Fetching updates from GitHub...
git fetch --all --verbose
if %errorlevel% neq 0 (
    echo Failed to fetch updates.

    goto run_script
)

echo Resetting local files to match remote main branch...
git reset --hard origin/main
if %errorlevel% neq 0 (
    echo Failed to reset files.

    goto run_script
)

echo Repository setup complete. Local directory is now synchronized with remote.


rem Check if ursina is installed
pip show ursina > nul 2>&1
if %errorlevel% equ 0 (
    echo Ursina is already installed.

) else (
    rem Install dependencies
    echo Installing dependencies...
    pip install -r requirements.txt
    echo Dependencies installed successfully.

)

:run_script
rem Run Python script
echo Running Python script...
start /B run.vbs

:end
