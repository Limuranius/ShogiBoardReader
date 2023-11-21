from enum import Enum


class BoardChangeStatus(Enum):
    INVALID_MOVE = "Invalid change"
    ILLEGAL_MOVE = "Illegal move"
    VALID_MOVE = "Valid move"
    NOTHING_CHANGED = "Board did not change"
