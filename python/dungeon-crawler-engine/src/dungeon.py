from __future__ import annotations

from random import random
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Literal, Optional


@dataclass(slots=True)
class Vector2D:

    x: float
    y: float

    def __add__(self, other: Vector2D) -> Vector2D:
        """
        Adds 2 vectors and returns a new vector object
        e.g. player.pos + Vector2D(0,1) -> move down
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2D) -> Vector2D:
        """
        Subtracts 2 vectors and returns a new vector object
        e.g. enemy.pos - player.pos → direction between them
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int | float) -> Vector2D:
        """
        Double the movement
        e.g. vec * 2
        """
        return Vector2D(self.x * scalar, self.y * scalar)

    def magnitude(self):
        """
        Distance from origin → used for aggro range checks
        """
        return (self.x**2 + self.y**2) ** 0.5

    def normalise(self):
        """
        Scale to length 1 → enemy "step" toward player
        """
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)


@dataclass
class Entity(ABC):

    name: str
    hp: int
    attack: int
    position: Vector2D

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

    @abstractmethod
    def act(self):
        pass


class Room:

    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.entities: list[Enemy] = []
        self.grid = self._generate()

    def _generate(self) -> list[list[str]]:
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]

        # Place walls randomly (~15% of tiles)
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) != (1, 1) and random() < 0.15:
                    grid[y][x] = "#"

        # Guarantee exit
        grid[self.height - 1][self.width - 1] = "E"
        return grid

    def is_walkable(self, pos: Vector2D) -> bool:
        x, y = int(pos.x), int(pos.y)
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.grid[y][x] != "#"

    def get_entities_at(self, pos: Vector2D) -> list[Enemy]:
        return [e for e in self.entities if e.position == pos]

    def get_tile(self, pos: Vector2D) -> str:
        return self.grid[int(pos.y)][int(pos.x)]

    def render(self, player: Player) -> str:
        rows = []

        for y in range(self.height):
            row = ""
            for x in range(self.width):
                pos = Vector2D(x, y)
                if player.position == pos:
                    row += "P"
                elif any(e.position == pos for e in self.entities):
                    row += "M"
                else:
                    row += self.grid[y][x]
            rows.append(row)
        return "\n".join(rows)


class Player(Entity):

    XP_PER_LEVEL: int = 100

    def __init__(
        self,
        name: str,
        hp: int,
        attack: int,
        position: Vector2D,
        gold: int = 0,
        xp: int = 0,
        inventory: list[str] = None,
    ):
        super().__init__(name, hp, attack, position)

        self.gold: int = gold
        self.xp: int = xp
        self.level: int = 1
        self.inventory = inventory if inventory is not None else []

    def move(self, direction: Vector2D, room: Room):
        """
        Takes a directions (Vector) and calculates the new position of the player
        Checks this new position against the room to see if it is valid before committing
        """
        new_pos = self.position + direction
        if room.is_walkable(new_pos):
            self.position = new_pos

    def gain_xp(self, amount: int):
        """
        Calculates the player's new xp after receiving some. If their xp is over the threshold, level up.
        """
        self.xp += amount
        if self.xp >= self.XP_PER_LEVEL:
            self._level_up()

    def _level_up(self):
        self.xp = 0
        self.level += 1
        self.hp += 10
        self.attack += 2
        print(f"Player has leveled up! Now level {self.level}")

    def attack_target(self, target: Enemy):
        target.take_damage(self.attack)

    def act(self):
        pass


class Enemy(Entity):

    def __init__(
        self,
        name: str,
        hp: int,
        attack: int,
        position: Vector2D,
        aggro_range: int = 5,
        xp_reward: int = 10,
    ):
        super().__init__(name, hp, attack, position)
        self.aggro_range = aggro_range
        self.xp_reward = xp_reward

    def act(self, player: Player):
        diff = player.position - self.position
        distance = diff.magnitude()

        if distance <= 1:
            # Adjacent attack
            player.take_damage(self.attack)
            print(f"{self.name} attacks {player.name} for {self.attack} damage")
        elif distance <= self.aggro_range:
            # Player in range -> move towards player
            step = diff.normalise()
            new_pos = self.position + Vector2D(round(step.x), round(step.y))
            self.position = new_pos


class Goblin(Enemy):
    def __init__(self, position: Vector2D):
        super().__init__(
            name="Goblin",
            hp=15,
            attack=3,
            position=position,
            aggro_range=4,
            xp_reward=50,
        )


class Troll(Enemy):
    def __init__(self, position: Vector2D):
        super().__init__(
            name="Troll",
            hp=40,
            attack=8,
            position=position,
            aggro_range=3,
            xp_reward=100,
        )


DIRECTIONS = {
    "w": Vector2D(0, -1),
    "s": Vector2D(0, 1),
    "a": Vector2D(-1, 0),
    "d": Vector2D(1, 0),
}


@dataclass(frozen=True, slots=True)
class Event:
    type: Literal["damage", "loot", "level_up"]
    target: Entity
    amount: Optional[int] = None
    item: Optional[str] = None


class GameEngine:

    def __init__(self, name: str, width: int = 10, height: int = 10):
        self.player = Player(name=name, hp=50, attack=10, position=Vector2D(1, 1))
        self.room = Room(width=width, height=height)
        self.event_queue: list[Event] = []
        self.running = False

        # Spawn some enemies
        self.room.entities = [Goblin(Vector2D(5, 5)), Troll(Vector2D(8, 8))]

    def queue_event(self, event: dict):
        self.event_queue.append(event)

    def process_events(self):
        for event in self.event_queue:
            match event.type:
                case "damage":
                    event.target.take_damage(event.amount)
                case "loot":
                    self.player.inventory.append(event.item)
                case "level_up":
                    self.player.gain_xp(100)

        self.event_queue.clear()

    def handle_input(self, user_input: str):
        if user_input in DIRECTIONS:
            self.player.move(DIRECTIONS[user_input], self.room)
        elif user_input == "attack":
            self._handle_attack()

    def _handle_attack(self):
        for entity in self.room.entities:
            diff = (entity.position - self.player.position).magnitude()
            if diff <= 1:
                event = Event(type="damage", target=entity, amount=self.player.attack)
                self.queue_event(event)
                print(
                    f"You attack {entity.name} for {self.player.attack} damage. {entity.name} remaining health: {entity.hp}"
                )

    def update(self):
        # Enemies act
        for entity in self.room.entities:
            entity.act(self.player)

        # Remove dead enemies, grant xp
        dead = [e for e in self.room.entities if not e.is_alive()]
        for e in dead:
            print(f"{e.name} defeated!")
            self.player.gain_xp(e.xp_reward)

        self.room.entities = [e for e in self.room.entities if e.is_alive()]

        # Process queued events
        self.process_events()

    def check_win_lose(self) -> str | None:
        if not self.player.is_alive():
            return "lose"
        if self.room.get_tile(self.player.position) == "E":
            return "win"
        return None

    def render(self):
        print("\033[2J\033[H")  # clear terminal
        print(self.room.render(self.player))
        print(
            f"\nHP: {self.player.hp} | ATK: {self.player.attack} | "
            f"Level: {self.player.level} | XP: {self.player.xp} | Gold: {self.player.gold}"
        )
        print("Move: w/a/s/d | Attack: attack | Quit: q")

    def run(self):
        self.running = True
        while self.running:
            self.render()
            user_input = input("> ").strip().lower()

            # Allow user to break out of the game
            if user_input == "q":
                break

            self.handle_input(user_input)
            self.update()

            result = self.check_win_lose()
            if result == "win":
                print("You escaped the dungeon")
                break
            elif result == "lose":
                print("You died!")
                break


if __name__ == "__main__":
    name = input("What is your name? ").strip().capitalize()
    game = GameEngine(name)
    game.run()
