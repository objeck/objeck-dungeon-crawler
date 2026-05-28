#!/usr/bin/env python3
"""Stage 2: method extraction + controller support for tiny_dungeon.obs"""
import sys

FNAME = 'C:/Users/objec/Documents/Code/objeck-dungeon-crawler/tiny_dungeon.obs'

with open(FNAME, 'r', newline='') as f:
    content = f.read()

original = content  # keep for diff reporting

# -----------------------------------------------------------------------
# STEP 1 - Add @controller : GameController; field
# -----------------------------------------------------------------------
OLD_FIELD = '\t@controller_open : Bool;\r\n\t@axis_cooldown'
NEW_FIELD = '\t@controller_open : Bool;\r\n\t@controller : GameController;\r\n\t@axis_cooldown'
assert OLD_FIELD in content, 'STEP 1 anchor not found'
content = content.replace(OLD_FIELD, NEW_FIELD, 1)
print('STEP 1 done')

# -----------------------------------------------------------------------
# STEP 2 - Add @controller := GameController->New(0) in init block
# -----------------------------------------------------------------------
OLD_INIT = '\t\t\t\t@controller_open := true;\r\n\t\t\t\t"[Controller] Gamepad detected"->ErrorLine();'
NEW_INIT = '\t\t\t\t@controller_open := true;\r\n\t\t\t\t@controller := GameController->New(0);\r\n\t\t\t\t"[Controller] Gamepad detected"->ErrorLine();'
assert OLD_INIT in content, 'STEP 2 anchor not found'
content = content.replace(OLD_INIT, NEW_INIT, 1)
print('STEP 2 done')

# -----------------------------------------------------------------------
# Helper: find the { ... } block following a search string
# Returns (brace_open, brace_close) indices (inclusive of braces)
# -----------------------------------------------------------------------
def find_block(text, search, start=0):
    idx = text.find(search, start)
    if idx < 0:
        raise ValueError(f'Anchor not found: {search[:60]!r}')
    brace_open = text.find('{', idx)
    depth = 1
    i = brace_open + 1
    while i < len(text) and depth > 0:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    return brace_open, i - 1  # (open_brace_pos, close_brace_pos)

# -----------------------------------------------------------------------
# STEP 3 - Extract label blocks into methods
# Order matters: extract from back to front so positions stay valid
# -----------------------------------------------------------------------

# --- Collect inner bodies (before any replacements) ---

# F7/Q flee
f7_open, f7_close = find_block(content, 'SDL_SCANCODE_F7')
inner_flee = content[f7_open+1 : f7_close]

# F6/Z spell
f6_open, f6_close = find_block(content, 'SDL_SCANCODE_F6')
inner_spell = content[f6_open+1 : f6_close]

# F5/P potion
f5_open, f5_close = find_block(content, 'SDL_SCANCODE_F5')
inner_potion = content[f5_open+1 : f5_close]

# F2/E read plaque
f2_open, f2_close = find_block(content, 'SDL_SCANCODE_F2')
inner_plaque = content[f2_open+1 : f2_close]

# SPACE confirm action (3rd occurrence - gameplay)
space_pos = 0
for _ in range(3):
    space_pos = content.find('SDL_SCANCODE_SPACE', space_pos + 1)
sp_open, sp_close = find_block(content, 'SDL_SCANCODE_SPACE', space_pos - 10)
inner_confirm = content[sp_open+1 : sp_close]

print(f'Collected inner blocks: confirm={len(inner_confirm)}, plaque={len(inner_plaque)}, '
      f'potion={len(inner_potion)}, spell={len(inner_spell)}, flee={len(inner_flee)}')

# --- Build method definitions ---
# We strip the leading/trailing whitespace of inner bodies and wrap them.
# Indentation inside the methods stays as-is (they'll compile fine).

def make_method(name, inner_body):
    return (
        f'\r\n\tmethod : {name}() ~ Nil {{\r\n'
        f'{inner_body}'
        f'\r\n\t}}\r\n'
    )

method_confirm = make_method('DoConfirmAction', inner_confirm)
method_plaque  = make_method('DoReadPlaque',    inner_plaque)
method_potion  = make_method('DoPotion',         inner_potion)
method_spell   = make_method('DoSpell',          inner_spell)
method_flee    = make_method('DoFlee',           inner_flee)

# --- Build GetControllerInput method ---
method_controller = r"""
	method : GetControllerInput(e : Event) ~ Nil {
		if(<>@controller_open) { return; };
		btn := e->GetJButton()->GetButton();

		# title screen
		if(@game_state = -1) {
			if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_A |
				btn = GameControllerButton->SDL_CONTROLLER_BUTTON_START) {
				@game_state := -2;
			}
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_BACK) {
				@quit := true;
			};
			return;
		};

		# class selection
		if(@game_state = -2) {
			if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_UP) {
				@class_cursor -= 1;
				if(@class_cursor < 0) { @class_cursor := 3; };
			}
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_DOWN) {
				@class_cursor += 1;
				if(@class_cursor > 3) { @class_cursor := 0; };
			}
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_A |
				btn = GameControllerButton->SDL_CONTROLLER_BUTTON_START) {
				@player := Player->New(@class_cursor);
				@game_state := 0;
				StartLevel(0);
			};
			return;
		};

		# terminal / game over
		if(@game_state = 1 | @game_state = 2) {
			if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_A |
				btn = GameControllerButton->SDL_CONTROLLER_BUTTON_START) {
				@game_state := -1;
			};
			return;
		};

		# puzzle
		if(@puzzle_active) {
			if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_UP)    { PuzzleInput(0); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_DOWN)  { PuzzleInput(1); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_LEFT)  { PuzzleInput(2); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_RIGHT) { PuzzleInput(3); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_BACK)  { @puzzle_active := false; };
			return;
		};

		# gameplay
		if(@game_state = 0 & @anim_counter = 0) {
			if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_A)           { DoConfirmAction(); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_B)      { DoFlee(); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_X)      { DoSpell(); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_Y)      { DoPotion(); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_RIGHTSHOULDER) { DoReadPlaque(); }
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_START)  {
				@quit := true;
			}
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_UP & @monster = Nil) {
				MoveForward();
				UpdateView();
			}
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_DOWN & @monster = Nil) {
				MoveLeft();
				MoveLeft();
			}
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_LEFT & @monster = Nil) {
				MoveLeft();
				UpdateView();
				UpdateCompass();
			}
			else if(btn = GameControllerButton->SDL_CONTROLLER_BUTTON_DPAD_RIGHT & @monster = Nil) {
				MoveRight();
				UpdateView();
				UpdateCompass();
			};
		};
	}

	method : PollController() ~ Nil {
		if(<>@controller_open | @controller = Nil) { return; };
		if(@game_state <> 0 | @monster <> Nil | @puzzle_active | @anim_counter <> 0) { return; };

		if(@axis_cooldown > 0) {
			@axis_cooldown -= 1;
			return;
		};

		dead_zone := 8000;
		threshold := 12000;

		ly := @controller->GetAxis(GameControllerAxis->SDL_CONTROLLER_AXIS_LEFTY);
		lx := @controller->GetAxis(GameControllerAxis->SDL_CONTROLLER_AXIS_LEFTX);

		if(ly < (dead_zone * -1) - threshold) {
			MoveForward();
			UpdateView();
			@axis_cooldown := 18;
		}
		else if(ly > dead_zone + threshold) {
			MoveLeft();
			MoveLeft();
			@axis_cooldown := 18;
		}
		else if(lx < (dead_zone * -1) - threshold) {
			MoveLeft();
			UpdateView();
			UpdateCompass();
			@axis_cooldown := 18;
		}
		else if(lx > dead_zone + threshold) {
			MoveRight();
			UpdateView();
			UpdateCompass();
			@axis_cooldown := 18;
		};
	}
"""

# -----------------------------------------------------------------------
# STEP 4 - Replace label block bodies with method calls (back-to-front)
# We work on the content from STEP 1+2 but positions were recorded before
# so we need to re-find them now.
# -----------------------------------------------------------------------

def replace_block_body(text, search_anchor, new_body_line, start_from=0):
    """Replace the { ... } body of a label block with a single call line."""
    idx = text.find(search_anchor, start_from)
    if idx < 0:
        raise ValueError(f'Anchor not found: {search_anchor[:60]!r}')
    brace_open = text.find('{', idx)
    depth = 1
    i = brace_open + 1
    while i < len(text) and depth > 0:
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
        i += 1
    brace_close = i - 1
    # build replacement: { \r\n\t\t\tCALL;\r\n        \t}
    new_block = '{\r\n        \t\t' + new_body_line + '\r\n        \t}'
    return text[:brace_open] + new_block + text[brace_close+1:]

# Replace F7 (flee) - furthest from start, do first so earlier positions unchanged
content = replace_block_body(content, 'SDL_SCANCODE_F7', 'DoFlee();')
print('STEP 4a: F7/Q -> DoFlee() done')

# Replace F6 (spell)
content = replace_block_body(content, 'SDL_SCANCODE_F6', 'DoSpell();')
print('STEP 4b: F6/Z -> DoSpell() done')

# Replace F5 (potion)
content = replace_block_body(content, 'SDL_SCANCODE_F5', 'DoPotion();')
print('STEP 4c: F5/P -> DoPotion() done')

# Replace F2 (plaque)
content = replace_block_body(content, 'SDL_SCANCODE_F2', 'DoReadPlaque();')
print('STEP 4d: F2/E -> DoReadPlaque() done')

# Replace SPACE (confirm) - 3rd occurrence
space_pos2 = 0
for _ in range(3):
    space_pos2 = content.find('SDL_SCANCODE_SPACE', space_pos2 + 1)
content = replace_block_body(content, 'SDL_SCANCODE_SPACE', 'DoConfirmAction();', space_pos2 - 5)
print('STEP 4e: SPACE -> DoConfirmAction() done')

# -----------------------------------------------------------------------
# STEP 5 - Insert extracted methods + controller methods before QPickAction
# -----------------------------------------------------------------------
QPICK_ANCHOR = '\r\n\tmethod : QPickAction() ~ Int {'
assert QPICK_ANCHOR in content, 'QPickAction anchor not found'

new_methods = (
    method_confirm +
    method_plaque  +
    method_potion  +
    method_spell   +
    method_flee    +
    method_controller
)

content = content.replace(QPICK_ANCHOR, new_methods + QPICK_ANCHOR, 1)
print('STEP 5 done: methods inserted before QPickAction')

# -----------------------------------------------------------------------
# STEP 6 - Add PollController() call in game loop before render_start
# -----------------------------------------------------------------------
OLD_RENDER = '\r\n\t\t\t\trender_start := Timer->GetTicks();\r\n\t\t\t\tRender(frame_count);'
NEW_RENDER = '\r\n\t\t\t\tPollController();\r\n\r\n\t\t\t\trender_start := Timer->GetTicks();\r\n\t\t\t\tRender(frame_count);'
assert OLD_RENDER in content, 'STEP 6 render_start anchor not found'
content = content.replace(OLD_RENDER, NEW_RENDER, 1)
print('STEP 6 done: PollController() call added')

# -----------------------------------------------------------------------
# Write output
# -----------------------------------------------------------------------
with open(FNAME, 'w', newline='') as f:
    f.write(content)

print(f'\nDone. File size: {len(content)} bytes (was {len(original)} bytes, delta +{len(content)-len(original)})')
