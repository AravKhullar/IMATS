from .base_agent import BaseAgent

class QLearningAgent(BaseAgent):
    def __init__(self, name, initial_cash):
        super().__init__(name, initial_cash)
        # Q-table and other parameters would be initialized here

    def act(self, market):
        """Decide action based on Q-learning policy."""
        pass

    def update(self, reward, new_state):
        pass 