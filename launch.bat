@echo off

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

rem Run Python script
echo Running Python script...
start /B run.vbs
