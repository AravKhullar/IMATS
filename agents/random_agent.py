from .base_agent import BaseAgent

class RandomAgent(BaseAgent):
    def act(self, market):
        """Randomly decide to buy, sell, or hold."""
        pass

    def update(self, reward, new_state):
        pass 