# Dungeon Crawler Engine

A terminal-based dungeon crawler built in Python with procedural room generation, turn-based combat, and a vector-based movement system.

## Project Structure

```Code
.
├── src/
│ ├── **init**.py
│ ├── vector.py
│ ├── entity.py
│ ├── player.py
│ ├── enemy.py
│ ├── room.py
│ └── game_engine.py
├── test_dungeon.py
└── README.md

```

## Setup

```bash
pip install pytest
```

## Running the Game

```bash
python -m src.game_engine
```

## Controls

| Input    | Action                |
| -------- | --------------------- |
| `w`      | Move up               |
| `s`      | Move down             |
| `a`      | Move left             |
| `d`      | Move right            |
| `attack` | Attack adjacent enemy |
| `q`      | Quit                  |

## Running Tests

```bash
pytest test_dungeon.py
```

## Classes

**`Vector2D`** — immutable 2D vector used for all positions and movement. Supports `+`, `-`, `*`, `magnitude()`, and `normalize()`.

**`Entity`** — abstract base class for all game characters. Holds `hp`, `attack`, `position`, and `name`.

**`Player`** — extends `Entity`. Moves via `room.is_walkable()` bounds checking. Gains XP and levels up every 100 XP (`+10 HP`, `+2 attack`).

**`Enemy`** — extends `Entity`. Acts each tick — moves toward player if within aggro range, attacks if adjacent. Subclasses: `Goblin` (low HP, fast), `Troll` (high HP, high damage).

**`Room`** — procedurally generated grid (`10x10`). Tiles: `.` floor, `#` wall, `E` exit.

**`GameEngine`** — main game loop (`input → update → render`). Processes a deferred event queue each tick for damage, loot, and level-up events.

## Win / Lose

- **Win**: reach the `E` exit tile
- **Lose**: HP reaches 0
