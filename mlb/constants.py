from enum import Enum


class Base(Enum):
    FIRST = "1b"
    SECOND = "2b"
    THIRD = "3b"


class InningState(Enum):
    TOP = "Top"
    BOTTOM = "Bottom"
