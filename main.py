import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from market import Market
from agents.random_agent import RandomAgent
from agents.q_learning_agent import QLearningAgent


def main():
    # Load historical price data (stub)
    price_data = pd.DataFrame()  # Replace with actual data loading

    # Initialize market
    market = Market(price_data)

    # Initialize agents
    agents = [
        RandomAgent("RandomAgent", initial_cash=10000),
        QLearningAgent("QLearningAgent", initial_cash=10000)
    ]

    # Track portfolio values
    portfolio_history = {agent.name: [] for agent in agents}

    # Simulation loop (stub)
    for step in range(100):  # Replace 100 with actual number of steps
        for agent in agents:
            action = agent.act(market)
            # Apply action to market/portfolio (stub)
            # ...
            # Calculate reward and update agent (stub)
            reward = 0
            agent.update(reward, None)
            # Track portfolio value (stub)
            portfolio_history[agent.name].append(agent.cash)  # Replace with actual portfolio value
        market.step()

    # Plot results
    for name, values in portfolio_history.items():
        plt.plot(values, label=name)
    plt.xlabel('Time Step')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.title('Agent Portfolio Values Over Time')
    plt.show()


if __name__ == "__main__":
    main() 