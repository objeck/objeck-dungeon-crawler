#!/usr/bin/env python3
"""Fix GetControllerInput: inline puzzle logic and fix Player->New signature."""

FNAME = 'C:/Users/objec/Documents/Code/objeck-dungeon-crawler/tiny_dungeon.obs'

with open(FNAME, 'r', newline='') as f:
    content = f.read()

# -----------------------------------------------------------------------
# Fix 1: Player->New("Warden", @class_cursor) in GetControllerInput
# -----------------------------------------------------------------------
OLD_PLAYER = '\t\t\t\t@player := Player->New(@class_cursor);\r\n\t\t\t\t@game_state := 0;\r\n\t\t\t\tStartLevel(0);'
NEW_PLAYER = '\t\t\t\t@player := Player->New("Warden", @class_cursor);\r\n\t\t\t\t@game_state := 0;\r\n\t\t\t\tStartLevel(0);'
assert OLD_PLAYER in content, 'Fix1: Player->New anchor not found'
content = content.replace(OLD_PLAYER, NEW_PLAYER, 1)
print('Fix 1 done: Player->New signature')

# -----------------------------------------------------------------------
# Fix 2: Replace placeholder puzzle block with inline rune-door logic
# -----------------------------------------------------------------------
OLD_PUZZLE = (
    '# puzzle\r\n'
    '\t\tif(@puzzle_active) {\r\n'
    '\t\t\tif(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_UP)    { PuzzleInput(0); }\r\n'
    '\t\t\telse if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_DOWN)  { PuzzleInput(1); }\r\n'
    '\t\t\telse if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_LEFT)  { PuzzleInput(2); }\r\n'
    '\t\t\telse if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_RIGHT) { PuzzleInput(3); }\r\n'
    '\t\t\telse if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_BACK)  { @puzzle_active := false; };\r\n'
    '\t\t\treturn;\r\n'
    '\t\t};\r\n'
)

NEW_PUZZLE = (
    '# rune door puzzle (puzzle_type=0)\r\n'
    '\t\tif(@puzzle_active & @puzzle_type = 0) {\r\n'
    '\t\t\tinput_dir := -1;\r\n'
    '\t\t\tif(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_UP)         { input_dir := 0; }\r\n'
    '\t\t\telse if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_DOWN)  { input_dir := 1; }\r\n'
    '\t\t\telse if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_RIGHT) { input_dir := 2; }\r\n'
    '\t\t\telse if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_LEFT)  { input_dir := 3; }\r\n'
    '\t\t\telse if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_BACK) {\r\n'
    '\t\t\t\t@puzzle_active := false;\r\n'
    '\t\t\t\t@puzzle_timer := 0;\r\n'
    '\t\t\t\treturn;\r\n'
    '\t\t\t};\r\n'
    '\t\t\tif(input_dir >= 0) {\r\n'
    '\t\t\t\tif(input_dir = @puzzle_sequence[@puzzle_input_pos]) {\r\n'
    '\t\t\t\t\t@puzzle_input_pos += 1;\r\n'
    '\t\t\t\t\tif(@puzzle_input_pos >= @puzzle_seq_len) {\r\n'
    '\t\t\t\t\t\t@puzzle_active := false;\r\n'
    '\t\t\t\t\t\t@puzzle_timer := 0;\r\n'
    '\t\t\t\t\t\t@map_manager->SetType(@player_location, MapManager->Type->OPEN);\r\n'
    '\t\t\t\t\t\t@view_type := MapManager->Type->OPEN;\r\n'
    '\t\t\t\t\t\t@can_show_item := false;\r\n'
    '\t\t\t\t\t\tgold_amount := 25 + @current_floor * 15 + Int->Random(0, 30);\r\n'
    '\t\t\t\t\t\t@player->AddGold(gold_amount);\r\n'
    '\t\t\t\t\t\t@reward_text->RenderedText("Rune door opens! +{$gold_amount} gold!", Color->New(100, 200, 255));\r\n'
    '\t\t\t\t\t\t@reward_timer := 60;\r\n'
    '\t\t\t\t\t\tRefreshStats();\r\n'
    '\t\t\t\t\t\tRefreshItems();\r\n'
    '\t\t\t\t\t}\r\n'
    '\t\t\t\t\telse {\r\n'
    '\t\t\t\t\t\tprogress := @puzzle_input_pos;\r\n'
    '\t\t\t\t\t\t@puzzle_text->RenderedText("{$progress}/{$@puzzle_seq_len} correct...", Color->New(100, 220, 100));\r\n'
    '\t\t\t\t\t\t@puzzle_timer := 60;\r\n'
    '\t\t\t\t\t};\r\n'
    '\t\t\t\t}\r\n'
    '\t\t\t\telse {\r\n'
    '\t\t\t\t\tdmg := 3 + @current_floor * 2;\r\n'
    '\t\t\t\t\t@player->UpdateHp(dmg);\r\n'
    '\t\t\t\t\t@damage_text->RenderedText("-{$dmg} Wrong sequence!", Color->New(255, 80, 40));\r\n'
    '\t\t\t\t\t@damage_timer := 30;\r\n'
    '\t\t\t\t\t@damage_is_player := true;\r\n'
    '\t\t\t\t\t@puzzle_active := false;\r\n'
    '\t\t\t\t\t@puzzle_timer := 0;\r\n'
    '\t\t\t\t\tRefreshStats();\r\n'
    '\t\t\t\t\tif(<>@player->IsAlive()) { @game_state := 1; ShowTerminalScreen(); };\r\n'
    '\t\t\t\t};\r\n'
    '\t\t\t};\r\n'
    '\t\t\treturn;\r\n'
    '\t\t};\r\n'
)

assert OLD_PUZZLE in content, 'Fix2: puzzle block anchor not found'
content = content.replace(OLD_PUZZLE, NEW_PUZZLE, 1)
print('Fix 2 done: puzzle block inlined')

with open(FNAME, 'w', newline='') as f:
    f.write(content)

print('Done')
