@echo off
setlocal
cd /d "%~dp0"
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
%PY% "%~dp0tools\kompose_tandem_orgo_ekole_p1_v2\installer.py" ROLLBACK
set "CODE=%ERRORLEVEL%"
if not "%CODE%"=="0" (echo [ECHEC] Code: %CODE% & pause)
exit /b %CODE%
