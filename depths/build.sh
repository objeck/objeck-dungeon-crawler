#!/bin/sh
# Builds (and optionally runs) the games in this folder.
#   ./build.sh depths   [brun]    Tiny Dungeon: Depths
#   ./build.sh gauntlet [brun]    Objeck Gauntlet
#   ./build.sh test               the two headless engine tests (no window needed)
# Expects the Objeck repository cloned next to this one, as ../../objeck-lang

cd "$(dirname "$0")" || exit 1
DEPLOY=../../objeck-lang/core/release/deploy
export PATH="$PATH:$DEPLOY/bin"
export OBJECK_LIB_PATH="$DEPLOY/lib"

ENGINE=dungeon_data.obs,dungeon_level.obs,dungeon_game.obs,dungeon_ai.obs
LOOK=dungeon_art.obs,dungeon_sound.obs,dungeon_view.obs
LIBS=sdl2,sdl_game,ai,json,collect

case "$1" in
  depths)
    obc -src $ENGINE,$LOOK,dungeon.obs -lib $LIBS -dest dungeon.obe || exit 1
    [ "$2" = "brun" ] && obr dungeon.obe
    ;;
  gauntlet)
    obc -src $ENGINE,$LOOK,gauntlet_game.obs,gauntlet.obs -lib $LIBS -dest gauntlet.obe || exit 1
    [ "$2" = "brun" ] && obr gauntlet.obe
    ;;
  test)
    obc -src $ENGINE,dungeon_tests.obs -lib ai,collect -dest dungeon_tests.obe || exit 1
    obr dungeon_tests.obe || exit 1
    obc -src $ENGINE,gauntlet_game.obs,gauntlet_tests.obs -lib ai,collect -dest gauntlet_tests.obe || exit 1
    obr gauntlet_tests.obe || exit 1
    ;;
  *)
    echo "usage: ./build.sh depths | gauntlet | test  [brun]"
    exit 1
    ;;
esac
