class BaseAgent:
    def __init__(self, name, initial_cash):
        self.name = name
        self.cash = initial_cash
        self.portfolio = {}

    def act(self, market):
        """Decide on an action given the current market state."""
        raise NotImplementedError

    def update(self, reward, new_state):
        """Update agent's internal state after taking an action."""
        raise NotImplementedError 