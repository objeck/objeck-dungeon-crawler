# Warden of Greyhold

A single-player Ultima-style fantasy RPG with a Wizardry-inspired first-person dungeon endgame, written entirely in [Objeck](https://github.com/objeck/objeck-lang). Procedurally generated, AI-narrated, fully animated with SDL2 primitives — no sprite sheets.

```
   The Order has fallen. The Seals of Binding crack.
   Malachar, the Undying, stirs in the Abyss.
   You alone remain.

                — Descend. Survive. End this. —
```

---

## Highlights

- **Top-down Ultima IV-style overworld** — 64×64 procedurally generated map with grass, forest, mountain, sea, towns, castles, bridges, and a skyport
- **First-person Wizardry-style dungeon** — 4 procedurally generated floors, 26+ hand-drawn monsters (SDL primitives, no sprites), trap-laden corridors, hidden rooms
- **Two vehicles** — buy a boat to sail the seas, or an airship to fly over everything
- **Living towns and castles** — weapon/armor shops, healer, inn, potion seller; castle lord with main quest
- **AI-driven narrative** — Ollama generates world name and threat, monster battle cries, level-up quips, victory epilogue, death epitaph, town merchant dialogue (async, never blocks gameplay)
- **Dynamic weather** — rotating Clear / Windy / Rain cycle with particle effects across overworld and encounter backgrounds
- **Full save/load** — JSON save persists player, position, vehicles, and dungeon state across sessions
- **4 player classes** — Knight (tank), Cleric (healer), Mage (caster), Ninja (crit specialist)
- **7-spell magic system** earned across 9 levels
- **8-tier weapon and armor progression**

---

## Quick Start

### Prerequisites

- [Objeck](https://github.com/objeck/objeck-lang) v2026.5.4 or newer, cloned as a sibling directory (`../objeck-lang`)
- SDL2, SDL2_image, SDL2_mixer, SDL2_ttf (bundled with Objeck deploy)
- Optional: [Ollama](https://ollama.com) running locally for AI narrative (game runs without it — AI features simply remain quiet)

### Build & Run (Windows)

```cmd
build.cmd brun
```

### Build & Run (Linux/macOS)

```bash
./build.sh
obr tiny_dungeon.obe
```

### Run Regression Tests

```powershell
tests/run_tests.ps1
```

Expected: `9/9 passed`.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       tiny_dungeon.obs                          │
│   Main game class — state machine, input, render dispatch,      │
│   combat resolution, save/load, town & castle UI                │
└────────┬──────────┬──────────────┬─────────────┬────────────────┘
         │          │              │             │
         ▼          ▼              ▼             ▼
   ┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
   │ dungeon │ │  dungeon │ │ dungeon  │ │  overworld   │
   │ managers│ │ entities │ │ monsters │ │   manager    │
   └─────────┘ └──────────┘ └──────────┘ └──────────────┘
   MapManager   Player        MonsterArt    WorldGen
   DungeonRend  Monster       (26 SDL       OverworldRend
   SoundMgr     Spell         drawings)     (animated,
   SpriteMgr    Weapon                       weather FX)
                Armor
                Potion
                                  ▼
                          ┌──────────────┐
                          │  dungeon_ai  │
                          └──────────────┘
                          AIWorker (thread)
                          Hash<String,String> cache
                          critical(mutex) sync
                          ─ battle cries
                          ─ level-up quips
                          ─ town messages
                          ─ castle speeches
                          ─ world generation
                          ─ victory / death narration
```

### Game States

| State | Meaning |
|-------|---------|
| `-1`  | Title screen |
| `-2`  | Class selection |
| `0`   | Dungeon (first-person 3D view) |
| `1`   | Game over |
| `2`   | Victory |
| `3`   | Overworld (top-down 2D view) |
| `4`   | Town interior menu |
| `5`   | Castle throne room |

---

## Player Manual

See **[MANUAL.md](MANUAL.md)** for the full player's guide: lore, classes, controls, combat, spells, items, monsters, and survival tips.

---

## Tech Notes

### AI Worker Thread Model

The `AIWorker` class in `dungeon_ai.obs` is a persistent background thread with:
- A `Queue<AIRequest>` for pending prompts
- A `Hash<String, String>` cache for completed responses
- A single `ThreadMutex` protecting both via `critical(@mutex) { }` blocks

This is the only thread synchronization primitive Objeck exposes (no condition variables, no semaphores), so the worker polls with `Thread->Sleep(10)` when idle.

Pre-warming: `PostFloorBattleCries(floor, class)` posts a request for every monster on that floor when `StartLevel()` is called. By the time the player encounters a Skeleton, its cry is usually already cached and appears with zero latency.

### Procedural Generation

- **Overworld** — `WorldGen` in `overworld_manager.obs` runs 7 passes: deep sea fill, continental mass, mountain ridges, coastline, forest patches, named locations (dungeon/castle/towns), and a dungeon approach path that guarantees reachability without breaking the coastline invariant.
- **Dungeon floors** — `MapManager->GenerateFloor` in `dungeon_managers.obs` uses randomized DFS maze carving + post-pass placement of treasure, traps, doors, secrets, mini-bosses, environmental features, bridges, and surface/up ladders on every floor (Floor 1's surface ladder exits to overworld).

### Rendering

All graphics are drawn with SDL2 primitives — no sprite sheets, no PNG assets. `MonsterArt` in `dungeon_monsters.obs` contains 26+ static draw functions composing each monster from filled circles, polygons, lines, and boxes. Wilderness backgrounds, overworld tiles, the player character, and the airship are all primitive-drawn and animated per frame.

---

## Source Layout

```
.
├── tiny_dungeon.obs       — Main game class (4000+ lines, all game state)
├── dungeon_managers.obs   — MapManager, DungeonRenderer, SoundManager
├── dungeon_eninities.obs  — Player, Entity, Monster, Spell, Weapon, Armor, Potion
├── dungeon_monsters.obs   — MonsterArt: 26+ SDL-primitive monster drawings
├── dungeon_ai.obs         — DungeonAI + AIWorker thread (async Ollama)
├── overworld_manager.obs  — WorldGen, OverworldManager, OverworldRenderer
├── build.cmd / build.sh   — Compilation scripts
├── build.json             — Source file + library manifest
├── sounds/                — WAV files (footsteps, strikes, coin pickup, music)
├── tests/                 — Regression test suite (9 tests, PowerShell runner)
├── README.md              — This file
└── MANUAL.md              — Player's guide
```

---

## Status

**v2026.5.4 release-aligned** — 9/9 regression tests passing. All design phases complete:

- ✓ Phase 1 — Overworld foundation (WorldGen + renderer + encounters)
- ✓ Phase 2 — Towns & economy
- ✓ Phase 3 — Vehicles (boat + airship)
- ✓ Phase 4 — Castles & quests
- ✓ Phase 5 — Save system
- ✓ Phase 6 — AI world generation
- ✓ Phase 7 — Polish & balance pass

---

## License

Built with the [Objeck programming language](https://github.com/objeck/objeck-lang).

```
   "The darkness awaits. Will you answer?"
```
