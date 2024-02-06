from abc import ABC, abstractmethod


class BaseAgent(ABC):
    r"""An abstract base class for all agents."""

    @abstractmethod
    def reset(self) -> None:
        r"""Resets the agent to its initial state."""
        pass

    @abstractmethod
    def step(self) -> None:
        r"""Performs a single step of the agent."""
        pass
