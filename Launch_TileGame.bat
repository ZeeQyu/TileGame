@echo off
REM Installs python 3.2.5 if not already installed and starts TileGame
REM // ZeeQyu

IF EXIST C:\Python32\ GOTO Game

ECHO Please install python using default settings.
msiexec.exe /i PythonInstaller\python-3.2.5.msi

:Game
C:\Python32\python.exe TileGame.py