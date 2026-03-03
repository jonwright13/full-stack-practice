import pytest
from dungeon import Vector2D, Player, Room, Goblin, Troll, Enemy

# ─── Vector2D ────────────────────────────────────────────────────────────────


def test_vector_addition():
    result = Vector2D(1, 2) + Vector2D(3, 4)
    assert result == Vector2D(4, 6)


def test_vector_normalization():
    result = Vector2D(3, 4).normalise()
    assert abs(result.magnitude() - 1.0) < 0.0001


def test_vector_magnitude():
    assert Vector2D(3, 4).magnitude() == 5.0


# ─── Entity ───────────────────────────────────────────────────────────────────


def test_entity_take_damage():
    player = Player("Hero", hp=50, attack=10, position=Vector2D(0, 0))
    player.take_damage(20)
    assert player.hp == 30


def test_entity_death():
    player = Player("Hero", hp=10, attack=10, position=Vector2D(0, 0))
    player.take_damage(999)
    assert player.hp == 0
    assert not player.is_alive()


# ─── Player ───────────────────────────────────────────────────────────────────


def test_player_levelup():
    player = Player("Hero", hp=50, attack=10, position=Vector2D(0, 0))
    player.gain_xp(100)
    assert player.level == 2
    assert player.hp == 60
    assert player.attack == 12


def test_player_move_out_of_bounds():
    room = Room(width=10, height=10)
    player = Player("Hero", hp=50, attack=10, position=Vector2D(0, 0))
    player.move(Vector2D(-1, 0), room)
    assert player.position == Vector2D(0, 0)


def test_player_move_into_wall():
    room = Room(width=10, height=10)
    room.grid[0][1] = "#"
    player = Player("Hero", hp=50, attack=10, position=Vector2D(0, 0))
    player.move(Vector2D(1, 0), room)
    assert player.position == Vector2D(0, 0)


# ─── Room ─────────────────────────────────────────────────────────────────────


def test_room_generation_has_exit():
    for _ in range(20):  # run multiple times since generation is random
        room = Room()
        has_exit = any("E" in row for row in room.grid)
        assert has_exit


# ─── Enemy ───────────────────────────────────────────────────────────────────


def test_enemy_aggro_range():
    goblin = Goblin(position=Vector2D(0, 0))
    player = Player("Hero", hp=50, attack=10, position=Vector2D(10, 10))
    goblin.act(player)
    assert goblin.position == Vector2D(0, 0)  # out of range, shouldn't move


def test_combat_round_reduces_hp():
    player = Player("Hero", hp=50, attack=10, position=Vector2D(0, 0))
    goblin = Goblin(position=Vector2D(1, 1))
    player.attack_target(goblin)
    assert goblin.hp == 5  # Goblin has 15 hp, player attack is 10
