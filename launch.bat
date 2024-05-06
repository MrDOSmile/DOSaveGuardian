@echo off

echo Running setup script...
call setup.bat

echo Running Python script...
start /B run.vbs

:end
