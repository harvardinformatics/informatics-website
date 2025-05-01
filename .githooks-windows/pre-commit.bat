@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0\pre-commit.ps1"
exit %ERRORLEVEL%