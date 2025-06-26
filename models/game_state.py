import copy
from typing import List, Optional
from itertools import combinations
from .person import Person
from .bridge import Bridge
from .flashlight import Flashlight
from .move import Move
from copy import deepcopy


class GameState:
    """
    Manages the current state of the bridge crossing puzzle game.
    Tracks positions of people, elapsed time, and win/lose conditions.
    """

    def __init__(self, bridge: Bridge, flashlight: Flashlight, all_persons: List[Person]):
        """
        Initialize the game state.

        Args:
            bridge (Bridge): The bridge object
            flashlight (Flashlight): The flashlight object
            all_persons (List[Person]): All people in the game
        """
        self._bridge = bridge
        self._flashlight = flashlight
        self._all_persons = all_persons.copy()

        self._left_side = all_persons.copy()
        self._right_side = []

        self._elapsed_time = 0
        self._game_won = False
        self._game_over = False
        self._move_history = []

        if self._all_persons:
            self._flashlight.give_to(self._all_persons[0])

    def get_left_side(self) -> List[Person]:
        return self._left_side.copy()

    def get_right_side(self) -> List[Person]:
        return self._right_side.copy()

    def get_elapsed_time(self) -> int:
        return self._elapsed_time

    def get_remaining_time(self) -> int:
        return max(0, self._bridge.get_max_time() - self._elapsed_time)

    def is_game_won(self) -> bool:
        return len(self._right_side) == len(self._all_persons)

    def is_game_over(self) -> bool:
        return self.is_game_won() or self._elapsed_time >= self._bridge.get_max_time()

    def get_flashlight_holder(self) -> Optional[Person]:
        return self._flashlight.get_current_holder()

    def get_move_history(self) -> List[Move]:
        return self._move_history.copy()

    def can_make_move(self, move: Move) -> bool:
        if self.is_game_over():
            return False

        if not move.is_valid(self._bridge):
            return False

        crossing_persons = move.get_crossing_persons()
        direction = move.get_direction()

        flashlight_holder = self._flashlight.get_current_holder()
        if not flashlight_holder:
            return False

        flashlight_side = self._left_side if flashlight_holder in self._left_side else self._right_side

        if not all(person in flashlight_side for person in crossing_persons):
            return False

        move_time = move.calculate_time(self._bridge)
        if self._elapsed_time + move_time > self._bridge.get_max_time():
            return False

        return True

    def make_move(self, move: Move) -> bool:
        if not self.can_make_move(move):
            return False

        crossing_persons = move.get_crossing_persons()
        direction = move.get_direction()

        if direction == "left_to_right":
            for person in crossing_persons:
                self._left_side.remove(person)
                self._right_side.append(person)
        else:
            for person in crossing_persons:
                self._right_side.remove(person)
                self._left_side.append(person)

        self._flashlight.give_to(crossing_persons[0])

        move_time = move.calculate_time(self._bridge)
        self._elapsed_time += move_time
        move.set_time_taken(move_time)
        self._move_history.append(move)

        self._game_won = self.is_game_won()
        self._game_over = self.is_game_over()

        return True

    def reset(self) -> None:
        self._left_side = self._all_persons.copy()
        self._right_side = []

        self._elapsed_time = 0
        self._game_won = False
        self._game_over = False
        self._move_history = []

        self._bridge.repair()

        if self._all_persons:
            self._flashlight.give_to(self._all_persons[0])

    def get_valid_moves(self) -> List[Move]:
        if self.is_game_over():
            return []

        valid_moves = []
        flashlight_holder = self.get_flashlight_holder()
        if not flashlight_holder:
            return []

        flashlight_side = self._left_side if flashlight_holder in self._left_side else self._right_side
        direction = "left_to_right" if flashlight_side is self._left_side else "right_to_left"

        for person in flashlight_side:
            move = Move([person], direction)
            if self.can_make_move(move):
                valid_moves.append(move)

        for p1, p2 in combinations(flashlight_side, 2):
            move = Move([p1, p2], direction)
            if self.can_make_move(move):
                valid_moves.append(move)

        return valid_moves

    def next_state(self, move: Move) -> Optional["GameState"]:
        if not move.is_valid(self._bridge):
            return None

        move_time = move.calculate_time(self._bridge)
        new_elapsed = self._elapsed_time + move_time
        if new_elapsed > self._max_time:
            return None

        new_state = deepcopy(self)

        crossing = frozenset(move.get_crossing_persons())
        if self._flashlight_side == "left":
            # Move from left to right
            if not crossing.issubset(new_state._left_side):
                return None
            new_state._left_side = new_state._left_side - crossing
            new_state._right_side = new_state._right_side.union(crossing)
            new_state._flashlight_side = "right"
        else:
            # Move from right to left
            if not crossing.issubset(new_state._right_side):
                return None
            new_state._right_side = new_state._right_side - crossing
            new_state._left_side = new_state._left_side.union(crossing)
            new_state._flashlight_side = "left"

        new_state._elapsed_time = new_elapsed
        return new_state

    def __str__(self) -> str:
        left_names = [p.get_name() for p in self._left_side]
        right_names = [p.get_name() for p in self._right_side]
        flashlight_holder = self.get_flashlight_holder()
        holder_name = flashlight_holder.get_name() if flashlight_holder else "None"

        return (f"Left: {left_names} | Right: {right_names} | "
                f"Time: {self._elapsed_time}/{self._bridge.get_max_time()} | "
                f"Flashlight: {holder_name}")

    def __repr__(self) -> str:
        return (f"GameState(left_side={len(self._left_side)}, right_side={len(self._right_side)}, "
                f"elapsed_time={self._elapsed_time}, game_won={self._game_won}, "
                f"game_over={self._game_over})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, GameState):
            return False
        return (
                self._bridge == other._bridge
                and self._flashlight == other._flashlight
                and set(self._left_side) == set(other._left_side)
                and set(self._right_side) == set(other._right_side)
                and self._elapsed_time == other._elapsed_time
                and self._game_won == other._game_won
                and self._game_over == other._game_over
                and self._move_history == other._move_history
                and set(self._all_persons) == set(other._all_persons)
        )

    def __hash__(self) -> int:
        # Hash based on bridge, flashlight, frozensets of sides, elapsed time and move history tuple
        return hash((
            self._bridge,
            self._flashlight,
            frozenset(self._left_side),
            frozenset(self._right_side),
            self._elapsed_time,
            self._game_won,
            self._game_over,
            tuple(self._move_history),
            frozenset(self._all_persons),
        ))

    def deepcopy(self):
        new_state = GameState(
            copy.deepcopy(self._bridge),
            copy.deepcopy(self._flashlight),
            copy.deepcopy(self._all_persons),
        )
        new_state._left_side = copy.deepcopy(self._left_side)
        new_state._right_side = copy.deepcopy(self._right_side)
        new_state._elapsed_time = self._elapsed_time
        new_state._game_won = self._game_won
        new_state._game_over = self._game_over
        new_state._move_history = copy.deepcopy(self._move_history)
        return new_state

