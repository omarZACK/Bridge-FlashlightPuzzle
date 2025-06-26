from typing import List
from . import Bridge
from .person import Person
import copy


class Move:
    """Represents a single crossing or return journey."""

    def __init__(self, crossing_persons: List[Person], direction: str):
        self._crossing_persons = crossing_persons.copy()
        self._direction = direction  # 'left_to_right' or 'right_to_left'
        self._time_taken = 0
        self._is_executed = False

    def get_crossing_persons(self) -> List[Person]:
        return self._crossing_persons.copy()

    def get_direction(self) -> str:
        return self._direction

    def get_time_taken(self) -> int:
        return self._time_taken

    def is_executed(self) -> bool:
        return self._is_executed

    def calculate_time(self, bridge: Bridge) -> int:
        return bridge.calculate_crossing_time(self._crossing_persons)

    def is_valid(self, bridge: Bridge) -> bool:
        return bridge.can_cross(self._crossing_persons)

    def execute(self, bridge: Bridge) -> bool:
        if not self.is_valid(bridge):
            return False
        self._time_taken = self.calculate_time(bridge)
        self._is_executed = True
        return True

    def set_time_taken(self, time: int) -> None:
        self._time_taken = time

    def get_person_names(self) -> List[str]:
        return [p.get_name() for p in self._crossing_persons]

    def __str__(self) -> str:
        names = ", ".join(self.get_person_names())
        arrow = "→" if self._direction == "left_to_right" else "←"
        tinfo = f" ({self._time_taken} min)" if self._is_executed else ""
        return f"{names} {arrow}{tinfo}"

    def __repr__(self) -> str:
        names = [p.get_name() for p in self._crossing_persons]
        return (
            f"Move(persons={names}, direction='{self._direction}', time_taken={self._time_taken}, "
            f"executed={self._is_executed})"
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Move)
            and self._crossing_persons == other._crossing_persons
            and self._direction == other._direction
        )

    def __hash__(self) -> int:
        # Use tuple of persons (assuming Person is hashable) and direction string
        return hash((tuple(self._crossing_persons), self._direction))

    def deepcopy(self):
        # Deepcopy persons list, copy direction, and primitive types
        new_move = Move(copy.deepcopy(self._crossing_persons), self._direction)
        new_move._time_taken = self._time_taken
        new_move._is_executed = self._is_executed
        return new_move
