# Python Challenge: Dungeon Crawler Engine

Build a terminal-based dungeon crawler with real-time-ish combat, procedural rooms, and a proper test suite.

---

## Core Concepts You Must Use

- **Classes**: `Vector2D`, `Entity`, `Player`, `Enemy`, `Room`, `GameEngine`
- **Multiple loops**: game loop, room generation loop, combat round loop, event queue loop
- **Vectors**: `Vector2D` class for position/movement math (add, subtract, magnitude, normalize)
- **Unit tests**: `unittest` or `pytest` — must cover vector math, combat logic, and room generation

---

## Spec

### `Vector2D`

- `__add__`, `__sub__`, `__mul__`, `magnitude()`, `normalize()`
- Used for all entity positions and movement deltas

### `Entity` (base class)

- `position: Vector2D`, `hp: int`, `attack: int`, `name: str`
- `is_alive()`, `take_damage(amount)`, abstract `act()`

### `Player(Entity)`

- Inventory list, gold count
- `move(direction: Vector2D)` — must validate bounds
- Level-up system (every 100 XP → +stats)

### `Enemy(Entity)`

- AI `act()` — moves toward player if within range, attacks if adjacent
- Different enemy types (Goblin, Troll, etc.) via subclasses or data

### `Room`

- Grid-based (`list[list[str]]`) — procedurally generated walls/enemies/loot
- `get_entities_at(pos: Vector2D)` method

### `GameEngine`

- Main game loop: input → update → render
- Event queue (list of dicts) processed each tick
- Win/lose conditions

---

## Test Requirements (min 10 tests)

```Python
test_vector_addition()
test_vector_normalization()
test_vector_magnitude()
test_entity_take_damage()
test_entity_death()
test_player_levelup()
test_player_move_out_of_bounds()
test_room_generation_has_exit()
test_enemy_aggro_range()
test_combat_round_reduces_hp()
```

---

## Deliverable

Single file `dungeon.py` + `test_dungeon.py`. Game should be **playable in terminal** with text input (`w/a/s/d` + `attack`).

---

## Stretch Goals

- Save/load state with `json`
- Pathfinding (BFS) for enemy AI
- Multiple floors with increasing difficulty

---

## Why This Is Hard

You'll need to wire the vector system into room bounds checking, manage an entity lifecycle across loops, write AI that reacts to player position, AND keep it testable without coupling everything together. The event queue pattern is a common game-dev pattern that trips people up.
