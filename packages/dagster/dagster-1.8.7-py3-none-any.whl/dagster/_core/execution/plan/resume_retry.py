import enum


class ReexecutionStrategy(enum.Enum):
    ALL_STEPS = "ALL_STEPS"
    FROM_FAILURE = "FROM_FAILURE"
