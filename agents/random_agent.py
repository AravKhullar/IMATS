from agents.base_agent import BaseAgent
import random

class RandomAgent(BaseAgent):
    def __init__(self, name, stocks):
        super().__init__(name)
        self.stocks = stocks

    def act(self, state):
        stock = random.choice(self.stocks)
        action = random.choice(["buy", "sell", "hold"])
        return {"stock" : stock, "action" : action}