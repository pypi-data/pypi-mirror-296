from typing import Protocol


class Comparable(Protocol):
    """Protocol for comparable objects."""

    def __lt__(self, other: "Comparable") -> bool:
        """Less than comparison."""
