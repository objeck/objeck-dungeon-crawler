# Warden of Greyhold — Ultima-Style Expansion Design

## Vision

A single-player fantasy RPG designed for a 3–4 hour complete playthrough. The world is
AI-generated at startup: Ollama creates the overworld layout, faction names, town descriptions,
and quest hooks so no two runs feel the same. The dungeon crawler (current game) becomes the
endgame — the player descends into Greyhold only after crossing the overworld and gathering
enough power to face the demon lord.

---

## World Structure

```
 Overworld (tiled, top-down, Ultima IV style)
   ├── 4–6 Towns    (shops, healers, NPCs with AI dialogue)
   ├── 2–3 Castles  (quest givers, throne rooms, royal guards)
   ├── Wilderness   (random encounters, resources, secrets)
   ├── Coastline    (docks → boat travel)
   ├── Sea tiles    (boat required; island dungeon access)
   └── Skyports     (airship docks; unlock late-game)
         └── Greyhold (the dungeon — current game, floors 1–4)
```

### Tile Types
| Type       | Walk | Boat | Airship | Notes |
|------------|------|------|---------|-------|
| Grass      | ✓    |      | fly over| default terrain |
| Forest     | ✓(slow)|    | fly over| random encounter rate +50% |
| Mountain   | ✗    |      | fly over| blocks ground movement |
| Shallow sea| ✗    | ✓    | fly over| requires boat |
| Deep sea   | ✗    | ✓    | fly over| sea monster encounters |
| Town       | ✓    |      |         | triggers town entry |
| Castle     | ✓    |      |         | triggers castle entry |
| Dungeon    | ✓    |      |         | triggers Greyhold |
| Skyport    | ✓    |      | dock    | board/disembark airship |

---

## AI-Generated World

At startup (background thread, same pattern as theme generation) Ollama produces:

```
WORLD: [world name, 3-5 words]
THREAT: [one-sentence backstory why Malachar must be stopped]
TOWN1: [name] | [2-word descriptor: e.g. "fishing village", "trading hub"]
TOWN2: [name] | [2-word descriptor]
...
CASTLE: [name] | [ruler name] | [one quest hook sentence]
QUEST1: [3-word title] | [one sentence description]
QUEST2: [3-word title] | [one sentence description]
```

This feeds:
- World map name shown on the overworld HUD
- NPC dialogue (merchants, castle rulers, healer greetings)
- Quest log entries
- Inn rest flavor text

---

## Game Phases & Pacing (3–4 hours)

| Phase | ~Time | Content |
|-------|-------|---------|
| **1. Origin** | 20 min | Class select → spawned outside a town → first NPC meets player → buys basic gear |
| **2. Exploration** | 60 min | Visit 2 towns, earn gold via encounters, find first map piece |
| **3. Castle Quest** | 40 min | Castle king tasks player with clearing a surface dungeon; rewards a key item |
| **4. Sea Voyage** | 30 min | Buy/find boat, sail to island, clear sea dungeon for second key item |
| **5. Sky Road** | 30 min | Airship unlocked (castle reward or hidden skyport); reach Greyhold's plateau |
| **6. Greyhold** | 60 min | Current dungeon, floors 1–4, AI boss Malachar |
| **7. Epilogue** | 5 min | AI-generated victory narrative, stats screen |

---

## Vehicles

### Boat
- Found docked at coastal towns or gifted after a quest
- `@has_boat : Bool`; triggers when standing on dock tile + E/action
- Navigation: same WASD/DPAD controls; only sea/shallow tiles passable
- Boarding animation: player sprite transitions to ship sprite
- Sea encounters: `MonsterID->SEA_SERPENT`, `MonsterID->KRAKEN`; same combat system

### Airship
- Unlocked mid-late game (castle reward or hidden skyport)
- `@has_airship : Bool`; can fly over all terrain except other airships/towns
- Faster movement (2 tiles per step)
- No random encounters while airborne
- Can only land on airship landing pads or open plains

---

## Towns

Each town is an 8×8 interior map with:

| Building    | Function |
|-------------|----------|
| Weapon Shop | Buy/sell weapons (tiered, floor-scaled) |
| Magic Shop  | Buy/sell spell scrolls |
| Inn         | Rest to full HP/MP (costs gold); AI-generated rest message |
| Healer      | Cure status ailments; AI-generated greeting |
| Tavern      | AI-generated rumor/hint; pay for info |
| Guild Hall  | Side quests; bounties |

Town NPC dialogue uses `DungeonAI->NpcLine(npc_role, player_class, floor)` — single-sentence
AI responses, same clip/trim pipeline as existing AI calls.

---

## Castles

Each castle has:
- Throne room with king/queen NPC (AI dialogue)
- Royal guard encounters (optional combat for "rogue" path)
- Quest board: 1 main + 1 side quest
- Treasury (locked; requires dungeon key item)

Castle quests drive the main plot: the king needs something from a dungeon; clearing it
advances the player toward Greyhold.

---

## Save System

Auto-save after every significant event:
- Entering/leaving a town or castle
- Completing a combat encounter
- Floor transitions inside Greyhold

Save file: `save.json` (JSON serialization of game state)

```json
{
  "version": 1,
  "player": { "class": 0, "hp": 42, "max_hp": 50, "gold": 130, ... },
  "overworld": { "x": 14, "y": 22, "has_boat": true, "has_airship": false },
  "quests": { "castle_quest": "complete", "sea_dungeon": "in_progress" },
  "world_seed": { "world_name": "Realm of Ashenveil", "threat": "...", ... }
}
```

The `world_seed` block is saved at startup so the same world persists across sessions.

---

## Technical Architecture

### New Classes

| Class | File | Purpose |
|-------|------|---------|
| `OverworldManager` | `overworld_manager.obs` | Tile map, camera scroll, encounters |
| `VehicleManager` | `vehicle_manager.obs` | Boat/airship state, boarding logic |
| `TownManager` | `town_manager.obs` | Town interiors, NPC placement |
| `CastleManager` | `castle_manager.obs` | Castle interiors, quest tracking |
| `QuestLog` | `quest_log.obs` | Active/completed quests, objectives |
| `SaveManager` | `save_manager.obs` | JSON serialize/deserialize game state |
| `WorldGen` | `world_gen.obs` | Procedural tile map, town/castle placement |

### Overworld Renderer
- Top-down tile renderer; 16×16 or 20×20 visible tiles
- Tiles are 24×24 pixel sprites from an overworld sprite sheet
- Player centered; map scrolls
- Day/night cycle (palette shift every N frames) for atmosphere

### Encounter System
- Wilderness tiles have per-tile encounter rate (forest > grass > coast)
- Step counter: every 8–16 steps on high-rate tiles roll for encounter
- Encounter zone table: coastal = sea monsters, forest = beast archetype, plains = mixed

### AI Extensions (DungeonAI)
Add to `dungeon_ai.obs`:
```objeck
function : NpcLine(role : String, player_class : String, floor : Int) ~ String
function : WorldGenPrompt() ~ String   # generates the full world seed block
function : QuestDesc(title : String) ~ String
function : InnMessage(world_name : String, player_class : String) ~ String
```

---

## Development Phases

### Phase 1 — Overworld Foundation (2–3 weeks)
- `WorldGen` produces a 64×64 tile map; place towns, castle, coast, dungeon entrance
- Top-down tile renderer with scrolling
- Player movement (keyboard + controller)
- Random encounter trigger → existing combat system
- No save yet; no towns

### Phase 2 — Towns & Economy (1–2 weeks)
- Town interior map + shop/healer/inn NPCs
- Gold economy tied to encounters
- AI NPC dialogue integration

### Phase 3 — Vehicles (1 week)
- Boat: dock detection, sea movement, sea encounters
- Airship: unlock via flag, fly-over logic, landing pad tiles

### Phase 4 — Castles & Quests (1–2 weeks)
- Castle interior + quest NPC
- Quest log UI
- Quest chain: castle → surface dungeon → sea dungeon → Greyhold

### Phase 5 — Save System (3–4 days)
- `SaveManager` with JSON read/write
- Auto-save triggers
- Continue from title screen

### Phase 6 — AI World Generation (3–4 days)
- World seed generation at startup (background thread)
- Wire AI names/lore into all NPC dialogue and map labels

### Phase 7 — Polish & Pacing (1 week)
- Play-test full 3–4 hour loop
- Balance gold economy, encounter rates, castle rewards
- Title screen reflects AI-generated world name
- Epilogue screen with AI narrative

---

## Out of Scope (v1)

- Multiplayer
- Procedural dungeon floors (Greyhold remains hand-designed)
- Crafting system
- Mounts (horse/dragon — add in v2 if wanted)
- Full voice / sound effects for NPC dialogue
