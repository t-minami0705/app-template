@echo off
setlocal EnableDelayedExpansion

rem =================================================================================
rem Example launcher
rem
rem arg1 : module name
rem
rem Example:
rem Run-Example.bat NemotronClient
rem =================================================================================

if "%~1"=="" (
    echo ERROR: Module name is required.
    echo Usage:
    echo   Run-Example.bat ^<ModuleName^>
    exit /b 1
)

set PACKAGE=%~1
for %%I in ("%~dp0.") do set "PROJECT_ROOT=%%~fI"
set EXAMPLE_ROOT=%PROJECT_ROOT%\examples

rem Search example script
set EXAMPLE_SCRIPT=

for /f "delims=" %%i in ('dir /b /s "%EXAMPLE_ROOT%\Ex-%PACKAGE%.ps1"') do (
    if "!EXAMPLE_SCRIPT!"=="" (
        set EXAMPLE_SCRIPT=%%i
    ) else (
        echo ERROR: Multiple example scripts found.
        echo !EXAMPLE_SCRIPT!
        echo %%i
        exit /b 1
    )
)

if "%EXAMPLE_SCRIPT%"=="" (
    echo ERROR: Example script not found.
    echo Target: Ex-%PACKAGE%.ps1
    exit /b 1
)

echo Example Script : %EXAMPLE_SCRIPT%
echo.

pwsh.exe -NoProfile -ExecutionPolicy Bypass ^
    -File "%EXAMPLE_SCRIPT%" ^
    -Package "%PACKAGE%" ^
    -ProjectRoot "%PROJECT_ROOT%"

endlocal