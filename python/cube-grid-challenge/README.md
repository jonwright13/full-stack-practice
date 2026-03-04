# 🧱 CubeGrid Challenge

## Overview

Build a class `CubeGrid` that simulates a falling-cube game on a 2D grid.

## Constructor

```Python
CubeGrid(width: number, height: number)
```

Initialises an empty grid of given dimensions.

## Core Method

```Python
drop(cubes: number[])
```

Accepts an array of **column indices** — each value represents a cube dropping into that column.

**Rules:**

- Cubes in the array drop **simultaneously** (process as one round)
- Each cube falls to the **lowest available row** in its column
- If a cube lands on top of another, it stacks upward
- After all cubes land, **any fully filled row is cleared** (Tetris-style)
- Rows above a cleared row **fall down** to fill the gap

## Additional Methods

```Python
getGrid(): (0 | 1)[][]     // returns current grid state, row 0 = bottom
getHeight(col: number): number  // returns current stack height in a column
```

---

## Example

```Python
grid = CubeGrid(4, 5)

grid.drop([0, 1, 2, 3])  // fills bottom row → clears immediately
grid.drop([0, 0, 1])     // col 0 gets 2 cubes stacked, col 1 gets 1
```

---

## Constraints

- Cubes dropped into a **full column** can be ignored or throw — your choice, but be explicit
- No gravity effects needed beyond stacking (no diagonal sliding)
- Grid height is fixed — define overflow behaviour yourself
