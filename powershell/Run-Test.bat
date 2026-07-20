@echo off
setlocal EnableDelayedExpansion

rem =================================================================================
rem Test launcher
rem
rem arg1 : module name
rem arg2 : start step number
rem
rem Example:
rem Run-Test.bat NemotronClient 3
rem =================================================================================

if "%~1"=="" (
    echo ERROR: Module name is required.
    echo Usage:
    echo   Run-Test.bat ^<ModuleName^> ^<StartStep^>
    exit /b 1
)

set PACKAGE=%~1
set START_STEP=%~2
for %%I in ("%~dp0.") do set "PROJECT_ROOT=%%~fI"
set TEST_ROOT=%PROJECT_ROOT%\tests

if "%START_STEP%"=="" (
    set START_STEP=1
)

rem Search test script
set TEST_SCRIPT=

for /f "delims=" %%i in ('dir /b /s "%TEST_ROOT%\Test-%PACKAGE%.ps1"') do (
    if "!TEST_SCRIPT!"=="" (
        set TEST_SCRIPT=%%i
    ) else (
        echo ERROR: Multiple test scripts found.
        echo !TEST_SCRIPT!
        echo %%i
        exit /b 1
    )
)

if "%TEST_SCRIPT%"=="" (
    echo ERROR: Test script not found.
    echo Target: Test-%PACKAGE%.ps1
    exit /b 1
)

echo Test Script : %TEST_SCRIPT%
echo Start Step  : %START_STEP%
echo.

pwsh.exe -NoProfile -ExecutionPolicy Bypass ^
    -File "%TEST_SCRIPT%" ^
    -Package "%PACKAGE%" ^
    -ProjectRoot "%PROJECT_ROOT%" ^
    -StartStep "%START_STEP%"

endlocal