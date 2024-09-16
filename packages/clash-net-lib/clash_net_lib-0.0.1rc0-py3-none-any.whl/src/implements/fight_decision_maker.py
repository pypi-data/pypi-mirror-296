"""An implementation of the DecisionMaker class for making decisions during a fight."""

from __future__ import annotations

from typing import TypedDict

import numpy as np

from src.decision_maker import Decision, DecisionInput, DecisionMaker

FightDecisionInputValue = np.ndarray

name = "Fight Decision"


class FightDecisionValue(TypedDict):
    """Represents the value of a fight decision."""

    cardIndex: int | None
    location: tuple[int, int] | None


class FightDecisionInput(DecisionInput[FightDecisionInputValue]):
    """Represents an input to a fight decision-making process."""

    def __init__(self, value: FightDecisionInputValue) -> None:
        """Initialize a FightDecisionInput instance.

        Args:
        ----
            value (FightDecisionInputValue): The value of the fight decision input.

        """
        super().__init__(name, value)


class FightDecision(Decision[FightDecisionValue]):
    """Represents a decision made during a fight."""

    def __init__(self, value: FightDecisionValue) -> None:
        """Initialize a FightDecision instance.

        Args:
        ----
            value (FightDecisionValue): The value of the fight decision.

        """
        super().__init__(name, value)


class FightDecisionMaker(DecisionMaker[FightDecisionInputValue, FightDecisionValue]):
    """An implementation of the DecisionMaker class for making decisions during a fight."""

    def __init__(self) -> None:
        """Initialize a FightDecisionMaker instance."""
        super().__init__()
