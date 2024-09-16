"""Decision-making module.

This module provides high-level classes for handling a decision-making process.
"""

from typing import TypeVar

DecisionName = str
DecisionInputValue = TypeVar("DecisionInputValue")
DecisionValue = TypeVar("DecisionValue")


class DecisionInput[DecisionInputValue]:
    """Represents an input to a decision-making process.

    Attributes
    ----------
        name (DecisionName): The name of the decision input.
        value (DecisionInputValue): The value of the decision input.

    """

    def __init__(self, name: str, value: DecisionInputValue) -> None:
        """Initialize a DecisionInput instance.

        Args:
        ----
            name (str): The name of the decision input.
            value (DecisionInputValue): The value of the decision input.

        """
        self.name: DecisionName = name
        self.value: DecisionInputValue = value

    def __str__(self) -> str:
        """Return a string representation of the DecisionInput.

        Returns
        -------
            str: The name and value of the decision input.

        """
        return self.name + " : " + str(self.value)

    def __repr__(self) -> str:
        """Return the official string representation of the DecisionInput.

        Returns
        -------
            str: The name and value of the decision input.

        """
        return self.__str__()


class Decision[DecisionValue]:
    """Represents a decision made based on inputs.

    Attributes
    ----------
        name (DecisionName): The name of the decision.
        value (DecisionValue): The value of the decision.

    """

    def __init__(self, name: str, value: DecisionValue) -> None:
        """Initialize a Decision instance.

        Args:
        ----
            name (str): The name of the decision.
            value (DecisionValue): The value of the decision.

        """
        self.name: DecisionName = name
        self.value: DecisionValue = value

    def __str__(self) -> str:
        """Return a string representation of the Decision.

        Returns
        -------
            str: The name and value of the decision.

        """
        return self.name + " : " + str(self.value)

    def __repr__(self) -> str:
        """Return the official string representation of the Decision.

        Returns
        -------
            str: The name and value of the decision.

        """
        return self.__str__()


class DecisionMaker[DecisionInputValue, DecisionValue]:
    """Manages decision inputs and generates decisions.

    Attributes
    ----------
        inputs (list[DecisionInput[DecisionInputValue]]): The list of inputs to the decision-making process.
        decisions (list[Decision[DecisionValue]]): The list of decisions made.

    """

    def __init__(self) -> None:
        """Initialize a DecisionMaker instance."""
        self.inputs: list[DecisionInput[DecisionInputValue]] = []
        self.decisions: list[Decision[DecisionValue]] = []

    def add_input(self, decision_input: DecisionInput[DecisionInputValue]) -> None:
        """Add an input to the decision-making process.

        Args:
        ----
            decision_input (DecisionInput[DecisionInputValue]): The decision input to be added.

        """
        self.inputs.append(decision_input)

    def make_decision(self) -> Decision[DecisionValue]:
        """Generate a decision based on the inputs.

        Raises
        ------
            NotImplementedError: If the method is not implemented.

        Returns
        -------
            Decision[DecisionValue]: The decision based on the inputs (when implemented).

        """
        msg = "make_decision method is not implemented"
        raise NotImplementedError(msg)
