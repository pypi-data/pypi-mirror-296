"""Enum representing the possible actions for the generator."""

from enum import Enum, auto


class Action(Enum):
    """Enum representing the possible actions for the generator."""

    UP = auto()
    UP_RIGHT = auto()
    # UP_LEFT = auto()
    DOWN = auto()
    DOWN_RIGHT = auto()
    # DOWN_LEFT = auto()
    RIGHT = auto()
    # LEFT = auto()


ALL_ACTIONS = list(Action)
