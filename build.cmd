@echo off

obc -src tiny_dungeon.obs,dungeon_managers.obs,dungeon_eninities.obs -lib gen_collect,sdl2,sdl_game,misc -dest tiny_dungeon.obe
IF NOT "%~1"=="" IF "%~1"=="brun"  (
	obr tiny_dungeon.obe
)