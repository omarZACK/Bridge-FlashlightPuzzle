from typing import List
from .person import Person


class Bridge:
    """Represents the bridge, with capacity and time constraints."""

    def __init__(self, capacity: int = 2, max_time: int = 17):
        self._capacity = capacity
        self._max_time = max_time
        self._is_destroyed = False

    def get_capacity(self) -> int:
        return self._capacity

    def get_max_time(self) -> int:
        return self._max_time

    def can_cross(self, persons: List[Person]) -> bool:
        """Return True if the bridge is intact and the group size ≤ capacity.
        Flashlight availability is enforced by `GameState`, so we do **not**
        check here whether one of the travellers currently holds it.
        """
        if self._is_destroyed or len(persons) == 0 or len(persons) > self._capacity:
            return False
        return True

    @staticmethod
    def calculate_crossing_time(persons: List[Person]) -> int:
        return max((p.get_crossing_time() for p in persons), default=0)

    def destroy(self) -> None:
        self._is_destroyed = True

    def is_passable(self) -> bool:
        return not self._is_destroyed

    def repair(self) -> None:
        self._is_destroyed = False

    def __str__(self) -> str:
        status = "destroyed" if self._is_destroyed else "passable"
        return f"Bridge (capacity: {self._capacity}, time limit: {self._max_time} min, status: {status})"

    def __repr__(self) -> str:
        return (
            f"Bridge(capacity={self._capacity}, max_time={self._max_time}, "
            f"is_destroyed={self._is_destroyed})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Bridge):
            return False
        return (
            self._capacity == other._capacity
            and self._max_time == other._max_time
            and self._is_destroyed == other._is_destroyed
        )

    def __hash__(self) -> int:
        return hash((self._capacity, self._max_time, self._is_destroyed))

    def deepcopy(self):
        new_bridge = Bridge(self._capacity, self._max_time)
        new_bridge._is_destroyed = self._is_destroyed
        return new_bridge
