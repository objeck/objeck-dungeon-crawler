@echo off
rem Builds (and optionally runs) the games in this folder.
rem   build.cmd depths   [brun]    Tiny Dungeon: Depths
rem   build.cmd gauntlet [brun]    Objeck Gauntlet
rem   build.cmd test               the two headless engine tests (no window needed)
rem Expects the Objeck repository cloned next to this one, as ..\..\objeck-lang

set DEPLOY=%~dp0..\..\objeck-lang\core\release\deploy-x64
set OBJECK_LIB_PATH=%DEPLOY%\lib
set PATH=%PATH%;%DEPLOY%\bin;%DEPLOY%\lib\sdl;%DEPLOY%\lib\native
cd /d %~dp0

set ENGINE=dungeon_data.obs,dungeon_level.obs,dungeon_game.obs,dungeon_ai.obs
set LOOK=dungeon_art.obs,dungeon_sound.obs,dungeon_view.obs
set LIBS=sdl2,sdl_game,ai,json,collect

if "%~1"=="" goto usage
if "%~1"=="depths" goto depths
if "%~1"=="gauntlet" goto gauntlet
if "%~1"=="test" goto test
:usage
echo usage: build.cmd depths ^| gauntlet ^| test  [brun]
exit /b 1

:depths
obc -src %ENGINE%,%LOOK%,dungeon.obs -lib %LIBS% -dest dungeon.obe || exit /b 1
if "%~2"=="brun" obr dungeon.obe
exit /b 0

:gauntlet
obc -src %ENGINE%,%LOOK%,gauntlet_game.obs,gauntlet.obs -lib %LIBS% -dest gauntlet.obe || exit /b 1
if "%~2"=="brun" obr gauntlet.obe
exit /b 0

:test
obc -src %ENGINE%,dungeon_tests.obs -lib ai,collect -dest dungeon_tests.obe || exit /b 1
obr dungeon_tests.obe || exit /b 1
obc -src %ENGINE%,gauntlet_game.obs,gauntlet_tests.obs -lib ai,collect -dest gauntlet_tests.obe || exit /b 1
obr gauntlet_tests.obe || exit /b 1
exit /b 0
