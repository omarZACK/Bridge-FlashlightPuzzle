from typing import Optional
from .person import Person
class Flashlight:
    """Single flashlight that can be passed between people."""

    def __init__(self):
        self._is_on = True
        self._current_holder: Optional[Person] = None

    def is_on(self) -> bool:
        return self._is_on

    def turn_on(self) -> None:
        self._is_on = True

    def turn_off(self) -> None:
        self._is_on = False

    def give_to(self, person: Person) -> None:
        if self._current_holder:
            self._current_holder.set_flashlight(False)
        self._current_holder = person
        person.set_flashlight(True)
        self.turn_on()

    def get_current_holder(self) -> Optional[Person]:
        return self._current_holder

    def take_from_current_holder(self) -> Optional[Person]:
        prev = self._current_holder
        if prev:
            prev.set_flashlight(False)
            self._current_holder = None
        return prev

    def is_held(self) -> bool:
        return self._current_holder is not None

    def __str__(self) -> str:
        return (
            f"Flashlight (held by {self._current_holder.get_name()})"
            if self._current_holder else "Flashlight (not held)"
        )

    def __repr__(self) -> str:
        holder = self._current_holder.get_name() if self._current_holder else None
        return f"Flashlight(is_on={self._is_on}, current_holder='{holder}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Flashlight):
            return False
        # Consider equal if is_on state and current_holder are equal
        return (self._is_on == other._is_on and
                self._current_holder == other._current_holder)

    def __hash__(self) -> int:
        # current_holder can be None; hash accordingly
        return hash((self._is_on, self._current_holder))

    def deepcopy(self):
        new_flashlight = Flashlight()
        new_flashlight._is_on = self._is_on
        # Deepcopy current holder if present, else None
        new_flashlight._current_holder = self._current_holder.deepcopy() if self._current_holder else None
        return new_flashlight
