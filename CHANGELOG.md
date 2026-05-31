# Changelog

All notable changes to **Warden of Greyhold**.

Format roughly follows [Keep a Changelog](https://keepachangelog.com/).
Versions track the Objeck runtime release this codebase is aligned with.

---

## [Unreleased]

Ongoing balance and polish work.

---

## [v2026.5.4-aligned] — 2026-05-31

### Added
- **Airship vehicle** — Buy at the skyport for 500g; flies over all terrain
  at 2× walking speed; SPACE/E to board, disembark, dock
- **Overworld save** — `save.json` now persists overworld position,
  `has_boat`, `has_airship`; LoadGame routes to dungeon or overworld
  based on where you saved
- **Auto-save** every 20 overworld steps, plus on vehicle purchases
- **Bridge tiles** for both overworld (stone arch + plank deck spanning
  narrow sea crossings, no boat needed) and dungeon (wood-plank floor
  over dark void in narrow corridors)
- **Animated overworld** — weather system (Clear / Windy / Rain rotating
  every 30–60s), drifting clouds, player walk cycle with bobbing cape
  and alternating legs, swaying grass blades and forest canopies, wind
  particles, rain streaks with ground ripples
- **Wilderness encounter backgrounds** — sky + ground scene replaces
  dungeon walls during surface fights; tile-appropriate (grass vs forest);
  weather effects layered over
- **Surface monster tables** — wilderness encounters use bandits,
  kobolds, wolves, and forest trolls instead of dungeon undead
- **Exit ladders** — Floor 1 `LATTER_DOWN` returns to overworld; deeper
  floors get an emergency exit in the middle of the map
- **Towns (Phase 2)** — weapon/armor shops with tier pricing, healer,
  inn (full rest), potion seller, boat purchase
- **Castles (Phase 4)** — lord NPC reads AI-generated threat; rewards
  boat to victors after 40+ kills
- **Async AI worker thread** — persistent background thread with
  `Queue<AIRequest>` + `Hash<String,String>` cache; `critical(mutex)`
  guards all access. Battle cries, level-up quips, town greetings,
  and castle speeches arrive within 1–2 seconds without ever blocking
  the render loop. Pre-warms on floor entry
- **Spell selection menu** — F6/Z opens a chooser instead of auto-casting
- **Continue saved game** — C on title screen
- **Regression test suite** — 9 unit tests covering JSON save/load,
  WorldGen, overworld passability, player class init, spells, items,
  combat math, town economy, vehicle / kill-threshold logic
- **5 new monsters** — Kobold, Banshee, Werewolf, Medusa, Nightmare
- **Tent key** (F8/T) — pitch a tent to fully restore HP/MP outside combat

### Changed
- **Player character redesigned** — rectangular armoured torso, distinct
  head, boots, cape, hat with feather, visible sword on hip — no longer
  resembles a peanut
- **Dungeon encounter rate** lowered to 9/11/13/15% for F1–F4
  (was 12/14/16/18%) for less combat-spam
- **Mimic chest** rate lowered to 10% (was 15%)
- **Gold rewards** now guarantee a minimum and scale better on deep floors
- **Text zones** reorganized — damage, reward, level-up, AI placard
  now occupy distinct, non-overlapping regions; AI placard suppressed
  while reward/level-up text is active
- **Castle lord speech** text wraps automatically to two lines
- **Overworld HUD** redesigned with 3-column, 2-row layout
- **Minimap** rewritten in SDL primitives (`map_0.png` removed entirely)
- **Procedural map generation** now guarantees a clear approach to the
  dungeon (clears mountains in a 5-tile radius + L-path from start;
  sea preserved for coastline integrity)
- **Theme generation** moved to background thread (`ThemeLoaderThread`),
  joined by `WorldGenLoaderThread` for AI world name + threat

### Fixed
- Overworld → dungeon transition no longer crashes due to uninitialized
  `@player_location` (StartLevel now called before game_state=0)
- Floor 1 `LATTER_DOWN` no longer crashes `@map_index` to -1; exits to
  overworld instead
- Dungeon fights show stone walls again (not the wilderness backdrop) —
  `@came_from_overworld` is now only set for surface random encounters
- Dungeon descent from the overworld no longer instantly returns you
  after a kill
- Items / treasure no longer respawn when turning in place
- Spell display, quest text, and AI placard no longer overlap

### Removed
- Sprite-based minimap (`map_0.png`)
- Sprite-based monster textures (`monsters_1.png`) — never used in
  the current renderer; removed legacy `SpriteManager` calls
- Old `images/` directory of Aseprite sources and PNGs
- Old `maps/debug.map` files (procedurally generated now)
- `design.md` planning document — all 7 phases complete
- Dead `@path` field in `MapManager` (referenced deleted `maps/debug.map`)

---

## [Pre-overhaul] — through 2026-05-27

The original tiny dungeon crawler. Sprite-based, fixed maps, single
game state. Replaced by the procedural Wizardry-style overhaul on
2026-05-27.
