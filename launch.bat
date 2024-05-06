@echo off

rem Set the directory where your repository is located
set REPO_DIR="https://github.com/MrDOSmile/DOSaveGuardian"

rem Check if Git is installed by trying to execute a Git command
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed.
    echo Opening browser to download Git...
    start https://git-scm.com/downloads
    goto end
)

rem Change to the repository directory
cd /D %REPO_DIR%

rem Check for repository existence
if not exist .git (
    echo This directory is not a Git repository.
    goto end
)

rem Check for internet connectivity
ping -n 1 google.com > nul 2>&1
if %errorlevel% neq 0 (
    echo No internet connection detected. Please check your network settings.
    goto run_script
)

rem Pull the latest changes from the repository
echo Pulling latest changes from GitHub...
git pull
if %errorlevel% neq 0 (
    echo Failed to pull from GitHub. Please check your Git configuration.
    goto run_script
)

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
