import pandas as pd

class Market:
    def __init__(self, price_data: pd.DataFrame):
        self.price_data = price_data.reset_index(drop=True)
        self.stocks = price_data.columns
        self.current_step = 0
        self.agents = {}

    def register_agent(self, name, starting_cash):
        self.agents[name] = {
            "cash": starting_cash,
            "shares": {stock: 0 for stock in self.stocks},
            "history": [],
        }

    def get_state(self):
        row = self.price_data.loc[self.current_step]
        prices = {stock: row[stock] for stock in self.stocks}
        return {
            "step": self.current_step,
            "prices": prices
        } 

    def step(self, agent_name, action):
        stock = action["stock"]
        action_type = action["action"]
        price = self.price_data.loc[self.current_step, stock]
        agent = self.agents[agent_name]
        
        if action_type == "buy" and agent["cash"] >= price:
            agent["shares"][stock] += 1
            agent["cash"] -= price
        elif action_type == "sell" and agent["shares"][stock] > 0:
            agent["shares"][stock] -= 1
            agent["cash"] += price
        elif action_type == "hold":
            pass
        
        value = self.get_agent_value(agent_name)
        agent["history"].append({
            "step": self.current_step,
            "stock": stock,
            "price": price,
            "shares": agent["shares"][stock],
            "cash": agent["cash"],
            "value": value
        })

    def next(self):
        self.current_step += 1
        return self.current_step < len(self.price_data)

    def get_agent_value(self, agent_name):
        agent = self.agents[agent_name]
        row = self.price_data.loc[self.current_step]
        prices = {stock: row[stock] for stock in self.stocks}
        return agent["cash"] + sum(agent["shares"][stock] * prices[stock] for stock in self.stocks)

    def get_history(self, agent_name):
        return self.agents[agent_name]["history"]