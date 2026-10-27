@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if errorlevel 1 goto :error
set "PY=python"
where py >nul 2>nul
if not errorlevel 1 set "PY=py -3"
set "PYTHONPATH=%~dp0src"
echo KOMPOSE B6 - simulation fictive de la boulangerie, SANS Orgo.
%PY% -m kompose.cli preview-kontexte "examples\kontexte-boulangerie\data\missions\boulangerie.json" "examples\kontexte-boulangerie\data\roles" --target-course qc-pri-ma-008 --replay "examples\kontexte-boulangerie\mock-orgo-receipts.json" --out "RESULTAT_B6_DEMO.json"
if errorlevel 1 goto :error
echo.
echo Resultat : RESULTAT_B6_DEMO.json
echo Aucun contact avec Orgo, aucune donnee d'eleve modifiee.
pause
exit /b 0
:error
echo ERREUR : verifie Python 3.10+ et les dossiers du pilote.
pause
exit /b 1
