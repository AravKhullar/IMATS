from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def act(self, state):
        """
        Decide what to do given the current market state.

        Parameters:
            state (dict): Contains current step, prices, etc.

        Returns:
            dict: Example: {"stock": "TSLA", "type": "buy"}
        """
        pass