```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              W A R D E N  O F  G R E Y H O L D           ║
║                                                          ║
║                  ~ A Dungeon of Darkness ~               ║
║                                                          ║
║                    Player's Manual                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

---

## THE STORY

For centuries, the Order of Wardens kept watch over the Seals of
Binding beneath the city of Greyhold. Deep below the cobblestone
streets and merchant quarters, ancient magic held a terrible evil
at bay — **Malachar, the Undying**, a demon lord imprisoned in the
Abyss since the First Age.

But the Order has fallen. Plague, war, and treachery have reduced
their numbers to one. **You.**

The Seals are cracking. The dead stir in the Catacombs. Spectral
horrors drift through the Forgotten Crypts. In the Deep Halls,
creatures of darkness sharpen their blades. And in the Abyss
itself, Malachar waits.

You must cross the wilderness, visit the towns and the castle to
gather strength, descend through four levels of the dungeon, and
face the Demon Lord before the Seals shatter completely and
darkness consumes the world above.

There is no army behind you. No reinforcements coming.

**Descend. Survive. End this.**

---

## THE WORLD

The realm has two layers:

```
   ┌──────────────────────────────────────────────────────┐
   │                  THE OVERWORLD                       │
   │  Top-down 64×64 world map with grass, forest,        │
   │  mountains, sea, two towns, a castle, a dungeon      │
   │  entrance, and a skyport. Random encounters in       │
   │  the wild. Weather rotates: clear, windy, rain.      │
   └──────────────┬───────────────────────────────────────┘
                  │  walk onto the dungeon tile
                  ▼
   ┌──────────────────────────────────────────────────────┐
   │                   GREYHOLD                           │
   │  Four floors of first-person procedural dungeon:     │
   │   F1: The Catacombs                                  │
   │   F2: The Forgotten Crypts                           │
   │   F3: The Deep Halls                                 │
   │   F4: The Abyss — Malachar's domain                  │
   └──────────────────────────────────────────────────────┘
```

Every world is procedurally generated. Every dungeon floor is
laid out fresh on each descent. Every save tells a different
story, and Ollama (if running) narrates yours with custom world
names, threats, battle cries, and a victory epilogue unique to
your run.

---

## CLASSES

Choose your path wisely. Each class brings different strengths
to the realm and the darkness below.

```
╔═══════════╦══════╦══════╦══════╦══════╦═══════════════════╗
║  CLASS    ║  HP  ║  STR ║  AGI ║  MP  ║  SPECIALTY        ║
╠═══════════╬══════╬══════╬══════╬══════╬═══════════════════╣
║  KNIGHT   ║ High ║ High ║  Med ║  Low ║ Best arms & armor ║
║  CLERIC   ║  Med ║  Med ║  Med ║ High ║ Healing & holy    ║
║  MAGE     ║  Low ║  Low ║  Med ║ VHig ║ Devastating magic ║
║  NINJA    ║  Med ║  Med ║ VHig ║  Low ║ Critical strikes  ║
╚═══════════╩══════╩══════╩══════╩══════╩═══════════════════╝
```

- **KNIGHT** — The stalwart shield. Knights have the most health
  and can equip the heaviest armor. Their raw strength makes
  every sword swing count. Best choice for new adventurers.
- **CLERIC** — The light in the dark. Clerics wield holy magic
  that heals wounds and smites the undead. Balanced stats and
  deep mana keep them fighting.
- **MAGE** — The arcane force. Fragile in body but devastating
  in mind. Mages have the largest mana reserves and learn the
  most powerful spells. One well-placed Inferno can end a fight.
- **NINJA** — The shadow blade. What the ninja lacks in brute
  force, they make up for in speed and precision. A 20% critical
  hit chance means every strike could be lethal.

---

## CONTROLS

### Overworld (top-down)

```
   MOVEMENT                     INTERACTION
   ════════                     ═══════════
   W / UP        Move north     SPACE / E   Board airship,
   S / DOWN      Move south                 dock, interact
   A / LEFT      Move west                  with tile
   D / RIGHT     Move east

   GAMEPAD: D-Pad moves, A button interacts/boards
```

Walking onto a `TOWN`, `CASTLE`, `DUNGEON`, or `SKYPORT` tile
opens its menu / interior automatically.

### Dungeon (first-person)

```
   MOVEMENT                     COMBAT
   ════════                     ══════
   W         Move forward       SPACE   Attack / Confirm
   A         Turn left          Z/F6    Open spell menu
   D         Turn right         P/F5    Use Potion
   S         Move backward      Q/F7    Flee
   E/F2      Read inscription   T/F8    Pitch tent (rest)
   F1        Search wall        ESC     Quit / cancel
```

Standing on a ladder shows context-sensitive hints in the bottom
strip. On Floor 1's surface staircase, the hint reads **"Ascend
to surface"** — pressing SPACE returns you to the overworld.

### Spell Menu (combat only)

```
   UP / DOWN     Navigate choices
   SPACE / RET   Cast selected spell
   ESC           Cancel — no MP spent
```

Spells you can't afford (insufficient MP) are dimmed.

### Town & Castle Menus

```
   UP / DOWN     Navigate
   SPACE / RET   Confirm
   1 – 7         Direct shortcuts
   ESC           Leave to overworld
```

---

## THE OVERWORLD

The map is yours to explore. Towns and the castle are roughly
visible on the horizon — you'll find them by walking.

### Tile Types

```
   GRASS      Walkable. ~6% encounter chance per step.
   FOREST     Walkable. ~12% encounter chance — beware of
              wolves, trolls, and werewolves.
   MOUNTAIN   Blocks ground movement; airship flies over.
   SHALLOW SEA Boat or airship only.
   DEEP SEA   Boat or airship only.
   BRIDGE     Walkable. Spans narrow sea crossings.
              No boat required.
   TOWN       Walk onto it to enter the town menu.
   CASTLE     Walk onto it to enter the throne room.
   DUNGEON    Walk onto it to begin your descent.
   SKYPORT    Buy / board / disembark an airship here.
```

### Weather

A weather cycle rotates every 30–60 seconds: **Clear**, **Windy**,
**Rain**. The HUD shows the current state. Windy weather adds
horizontal streaks; Rain falls in diagonal sheets with ground
ripples. Weather is visible both on the overworld and during
wilderness encounters.

While riding the airship the HUD shows **"Airborne"** instead.

### Encounters

Surface monsters differ from dungeon monsters — you'll meet
**bandits**, **kobold scouts**, **dire wolves**, and **forest
trolls** in the wild, not undead. The encounter background
matches the terrain (grassland skies vs forest canopy), with
weather effects layered over.

When a monster appears you drop into the same combat system
used in the dungeon. Winning or fleeing returns you to the
overworld where you were standing.

---

## TOWNS

Walk onto a town tile to enter its menu:

```
   1. Weapon Shop      Buy the next weapon tier
                       (50g + tier × 30g)
   2. Armor Shop       Buy the next armor tier
                       (40g + tier × 25g)
   3. Healer           Restore HP + MP + clear status
                       (2g per missing HP, min 10g)
   4. Inn              Rest to full
                       (30g flat, AI rest message)
   5. Potions          Buy a health potion
                       (10g each)
   6. Boat             Purchase a boat
                       (200g — sail the seas)
   7. Leave town
```

The tavern keeper may share a cryptic rumor on the main menu
(if AI is available). Press ESC at any time to step back outside.

---

## THE CASTLE

The castle lord oversees the realm and will speak of the threat
when you address him. He recognizes a true hero after you've
proven yourself in the dungeon (40+ kills) — once that's done,
he will reward you with a boat if you don't already have one.

```
   1. Speak with the Lord    Hear about the threat / receive
                             your reward if you've earned it
   2. Boat                   Gift of the realm
   3. Leave castle
```

---

## VEHICLES

### Boat

Bought at any town for **200g**, or gifted by the castle lord
after proving yourself. With a boat you can sail across both
shallow and deep sea tiles. Mountains still block you.

### Airship

Bought at the **skyport** for **500g**. With an airship you
can:
- Fly over **any** terrain — mountains, deep sea, anything
- Move at **double speed** (3-frame cooldown vs 6 walking)
- Avoid all wilderness encounters while airborne

Press **SPACE / E** while standing on the skyport to board,
or anywhere over open ground to land. You cannot land on
sea tiles — find solid ground first. The HUD changes to
**"Airborne"** while flying. A 3-airship-icon walk cycle
shows propellers spinning and a shadow on the ground below.

```
       ╭─────────╮
      ╱ /█████/ ╲       The airship — red balloon with
     │  /███/   │       seam panels, wooden gondola with
      ╲ ─────── ╱       porthole window, twin propellers,
       │  ▢  │          and a ground shadow indicating
       └─────┘          altitude.
       ◯     ◯
```

---

## COMBAT

When a monster appears, combat begins. Trade blows until one
of you falls.

- **Attack (SPACE)** — Strike with your equipped weapon. Damage
  is calculated from Strength, Agility, and weapon hit value.
  Knights excel; Ninjas may crit for double damage.
- **Spell (Z/F6)** — Opens the spell chooser panel. Pick a
  spell with UP/DOWN, cast with SPACE. Heal restores HP;
  damage spells bypass armor.
- **Potion (P/F5)** — Drink an inventory potion. The monster
  gets a free attack while you drink, so time it carefully.
- **Flee (Q/F7)** — Run from non-boss fights. Flee chance scales
  with Agility (Ninjas escape most easily). Failed flee gives
  the monster a free strike.

Battle cries, level-up quips, and atmospheric placards are
generated by Ollama in the background and appear in a gold-
framed parchment when ready. They never block gameplay — if
the worker hasn't responded yet, the text simply doesn't
appear until next time.

---

## EQUIPMENT

Equipment improves with descent and at town shops.

```
   WEAPONS                         ARMOR
   ═══════                         ═════
   Tier 0: Fists                   Tier 0: Rags
   Tier 1: Rusty Dagger            Tier 1: Leather Tunic
   Tier 2: Short Sword             Tier 2: Studded Leather
   Tier 3: Mace                    Tier 3: Chain Mail
   Tier 4: Longsword               Tier 4: Plate Mail
   Tier 5: Battle Axe              Tier 5: Dragon Scale
   Tier 6: Flaming Sword           Tier 6: Mithril Plate
   Tier 7: Holy Avenger            Tier 7: Blessed Armor
```

New equipment from chests is automatically equipped if better
than what you carry. Town shops always sell you the **next tier
up** from what you currently wield.

---

## SPELLS

Spells are learned automatically on level-up. Each costs mana
(MP) to cast. MP regenerates slowly as you walk (1 MP per 10
steps). Tents fully restore both HP and MP.

```
   LEVEL  SPELL          MP    EFFECT
   ═════  ═════          ══    ══════
     1    Heal            3    Restore 15 HP
     2    Flame           5    20 fire damage
     3    Frost           5    18 ice damage
     4    Shield          4    +25 defense (temporary)
     5    Lightning       8    35 damage
     7    Holy Smite     12    50 damage (1.5× vs undead)
     9    Inferno        20    80 fire damage
```

Knights start with Heal; Clerics start with Heal; Mages start
with Flame at level 2; Ninjas start with no spells. The spell
chooser highlights the selected entry in gold and dims any
spell whose MP cost you can't currently afford.

---

## ITEMS

- **Health Potions** — Restore HP. Found on the ground,
  dropped by monsters, or bought at towns for 10g. Press
  P or F5 to use.
- **Tents** — Pitch a tent with T or F8 to fully restore
  HP and MP. Tents are consumed on use and can only be
  used outside combat.
- **Antidotes / Cures** — The healer at any town clears all
  status effects (poison, blindness, confusion, curses) for
  her standard fee.

---

## MONSTERS

### The Wilderness (overworld)

```
   GRASSLAND            FOREST
   ═════════            ══════
   Wild Rat             Giant Spider
   Giant Bat            Dire Wolf
   Kobold Scout         Forest Troll
   Highwayman           Bandit Archer
   Road Bandit          Kobold Shaman
   Giant Spider         Werewolf
```

### The Dungeon

```
   F1: THE CATACOMBS    F2: THE FORGOTTEN CRYPTS
   ════════════         ════════════════════════
   Giant Rat            Spectral Ghost
   Cave Bat             Hollow Wraith
   Skeleton Warrior     Grave Ghoul
   Dungeon Spider       Dark Priest
   Shambling Zombie     Living Shadow
   Mushroom Fiend       Vampire
   Kobold               Banshee

   F3: THE DEEP HALLS   F4: THE ABYSS
   ══════════════       ═════════════
   Hill Ogre            Pit Demon
   Cave Troll           Hellhound
   Dark Knight          Dark Sorcerer
   Stone Gargoyle       Ancient Dragon
   Undead Lich          Balor
   Werewolf             Eye Tyrant
   Medusa               Nightmare

   BOSS: MALACHAR, THE UNDYING
   The demon lord imprisoned in the Abyss.
   The final seal. The end of all things.
   Or the beginning of your legend.
```

### Mini-Bosses

Each dungeon floor has a chance of spawning a champion variant
of one of its monsters — bigger, tougher, and guaranteed to
drop a tier-up weapon or armor when defeated.

---

## SAVE & LOAD

The game auto-saves:
- After every monster kill
- After every floor transition (descend or ascend)
- Every 20 overworld steps
- On airship purchase, boat purchase, and skyport docking

Your save file `save.json` lives next to the executable. To
resume, press **C** on the title screen — the option appears
only if a save exists. You'll resume in the same state, on the
same tile or dungeon floor, with your full inventory, gear,
gold, and vehicles.

Winning the game (defeating Malachar) clears the save — the
next launch starts fresh.

---

## TIPS FOR SURVIVAL

- **Visit the town first.** Even a tier-up sword and an inn
  rest before descending gives you a huge edge in the Catacombs.
- **Save your potions.** Don't waste them on Wild Rats. Hoard
  for boss fights and emergencies.
- **Read every inscription.** Plaques give hints about traps,
  puzzles, and Malachar's weaknesses.
- **The castle lord's reward is worth getting.** Even if you
  buy your own boat, clear the dungeon and return — he gives
  you something only victors can earn.
- **Watch the weather.** Heavy rain doesn't slow you, but it
  does signal the storms of the deeper realm.
- **The airship is endgame.** 500g is a lot, but flying past
  every encounter to reach Greyhold is the fastest path.
- **Level up before descending.** Each floor is harder than
  the last. Ninja crits help on F1–F2; bring a Cleric's Holy
  Smite for F2; Knight's gear matters more on F3–F4.
- **Mages are fragile but devastating.** Stay healed and
  unleash spells strategically. Inferno can one-shot most
  F3 monsters.

---

## CREDITS

```
   WARDEN OF GREYHOLD
   A Wizardry-meets-Ultima dungeon crawler

   Built with the Objeck programming language
   SDL2 graphics, audio, and primitives

   Procedurally generated overworld and dungeon
   AI-narrated quests, battle cries, and epilogue (Ollama)
   Hand-drawn SDL-primitive monster art (26+ creatures)
   Synthesized chiptune soundtrack

   "The darkness awaits. Will you answer?"
```

---

*This manual is best read by torchlight.*
