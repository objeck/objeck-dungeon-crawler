@echo off

set OBJECK_LIB_PATH=..\objeck-lang\core\release\deploy-x64\lib
set PATH=%PATH%;..\objeck-lang\core\release\deploy-x64\bin;..\objeck-lang\core\release\deploy-x64\lib\sdl

obc -src tiny_dungeon.obs,dungeon_managers.obs,dungeon_eninities.obs,dungeon_monsters.obs,dungeon_ai.obs -lib cipher,net,gen_collect,sdl2,json,sdl_game,misc,ollama -dest tiny_dungeon.obe
IF NOT "%~1"=="" IF "%~1"=="brun"  (
	obr tiny_dungeon.obe
)