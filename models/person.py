class Person:
    """Represents a person in the bridge crossing puzzle."""

    def __init__(self, name: str, crossing_time: int):
        self._name = name
        self._crossing_time = crossing_time
        self._has_flashlight = False

    def get_name(self) -> str:
        return self._name

    def get_crossing_time(self) -> int:
        return self._crossing_time

    def set_flashlight(self, has_flashlight: bool) -> None:
        self._has_flashlight = has_flashlight

    def has_flashlight(self) -> bool:
        return self._has_flashlight

    def __str__(self) -> str:
        flashlight_status = " (with flashlight)" if self._has_flashlight else ""
        return f"{self._name} ({self._crossing_time} min){flashlight_status}"

    def __repr__(self) -> str:
        return (
            f"Person(name='{self._name}', crossing_time={self._crossing_time}, "
            f"has_flashlight={self._has_flashlight})"
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Person) and
            self._name == other._name and
            self._crossing_time == other._crossing_time and
            self._has_flashlight == other._has_flashlight
        )

    def __hash__(self) -> int:
        return hash((self._name, self._crossing_time, self._has_flashlight))

    def deepcopy(self):
        # Create a deep copy of this person instance
        new_person = Person(self._name, self._crossing_time)
        new_person.set_flashlight(self._has_flashlight)
        return new_person