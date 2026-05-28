@echo off
cd /d "%~dp0"

set OBC=..\..\..\objeck-lang\core\release\deploy-x64\bin\obc.exe
set OBR=..\..\..\objeck-lang\core\release\deploy-x64\bin\obr.exe
set OBJECK_LIB_PATH=..\..\..\objeck-lang\core\release\deploy-x64\lib
set PATH=%PATH%;..\..\..\objeck-lang\core\release\deploy-x64\bin;..\..\..\objeck-lang\core\release\deploy-x64\lib\sdl

set GAME_SRC=..\dungeon_managers.obs,..\dungeon_eninities.obs,..\dungeon_monsters.obs,..\dungeon_ai.obs,..\overworld_manager.obs
set LIBS=cipher,net,gen_collect,sdl2,json,sdl_game,misc,ollama

set PASS=0
set FAIL=0
set BUILD_FAIL=0

echo ============================================================
echo  Warden of Greyhold — Regression Test Suite
echo ============================================================
echo.

REM --- test_saveload (SDL-free: only json+filesystem) ---
call :RunTest test_saveload json,misc
call :RunTest test_worldgen %LIBS%
call :RunTest test_overworld %LIBS%
call :RunTest test_player    %LIBS%
call :RunTest test_spells    %LIBS%
call :RunTest test_items     %LIBS%
call :RunTest test_combat    %LIBS%

echo.
echo ============================================================
echo  Results: %PASS% passed, %FAIL% failed, %BUILD_FAIL% build errors
echo ============================================================
if %FAIL% GTR 0 exit /b 1
if %BUILD_FAIL% GTR 0 exit /b 2
exit /b 0

:RunTest
set TEST=%~1
set TEST_LIBS=%~2
echo --- %TEST% ---

REM Build
if "%TEST%"=="test_saveload" (
    "%OBC%" -src %TEST%.obs -lib %TEST_LIBS% -dest %TEST%.obe 2>&1
) else (
    "%OBC%" -src %TEST%.obs,%GAME_SRC% -lib %TEST_LIBS% -dest %TEST%.obe 2>&1
)

if errorlevel 1 (
    echo   BUILD FAILED
    set /A BUILD_FAIL+=1
    goto :eof
)

REM Run and capture output
"%OBR%" %TEST%.obe > %TEST%.out 2>&1
type %TEST%.out

REM Check for FAIL in output
findstr /C:"FAIL" %TEST%.out >nul
if errorlevel 1 (
    set /A PASS+=1
) else (
    set /A FAIL+=1
)

del %TEST%.obe %TEST%.out 2>nul
goto :eof
