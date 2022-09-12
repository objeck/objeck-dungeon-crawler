export PATH=$PATH:../objeck-lang/core/release/deploy/bin
export OBJECK_LIB_PATH=../objeck-lang/core/release/deploy/lib

obc -src tiny_dungeon.obs,dungeon_managers.obs,dungeon_eninities.obs -lib gen_collect,sdl2,json,sdl_game,misc -dest tiny_dungeon.obe
if [ ! -z "$1" ] && [ "$1" = "brun" ]; then
	obr tiny_dungeon.obe
fi;


