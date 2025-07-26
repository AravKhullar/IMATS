from agents.base_agent import BaseAgent
import random

class QLearningAgent(BaseAgent):
    def __init__(self, name, stocks, alpha = 0.1, gamma = 0.95, epsilon = 0.1):
        super().__init__(name)
        self.stocks = stocks
        self.alpha = alpha #Learning Rate
        self.gamma = gamma #Discount Factor
        self.epsilon = epsilon #Exploration Rate
        self.q_table = {}
        self.last_state = None
        self.last_action = None

    def get_q(self, state_key, action):
        return self.q_table.get((state_key, action), 0.0)

    def act(self, state):
        sentiment = state.get("sentiment", 0)
        state_key = tuple(round(state["prices"][stock], -1) for stock in self.stocks) + (sentiment,)
        possible_actions = []
        for stock in self.stocks:
            possible_actions.extend([
                (stock, "buy"),
                (stock, "sell"),
                (stock, "hold")
            ])
        if random.random() < self.epsilon:
            action = random.choice(possible_actions)
        else:
            q_values = [self.get_q(state_key, a) for a in possible_actions]
            maxq = max(q_values)
            best_actions = [a for a, q in zip(possible_actions, q_values) if q == maxq]
            action = random.choice(best_actions)
        
        self.last_state = state_key
        self.last_action = action
        return {"stock": action[0], "action": action[1]}

    def update(self, reward, new_state):
        if self.last_state is None or self.last_action is None:
            return
        sentiment = new_state.get("sentiment", 0)
        new_state_key = tuple(round(new_state["prices"][stock], -1) for stock in self.stocks) + (sentiment,)
        future_qs = [
            self.get_q(new_state_key, (s, a))
            for s in self.stocks
            for a in ["buy", "sell", "hold"]
        ]
        max_future_q = max(future_qs)
        old_q = self.get_q(self.last_state, self.last_action)
        updated_q = old_q + self.alpha * (reward + self.gamma * max_future_q - old_q)
        self.q_table[(self.last_state, self.last_action)] = updated_q
        
        self.last_action = None
        self.last_state = None
