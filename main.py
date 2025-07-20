from market import Market
from agents.random_agent import RandomAgent
from agents.q_learning_agent import QLearningAgent
import tools
import os


def main():
    data = tools.load_stock_data("data/stock_prices.csv")
    stock_list = list(data.columns)
    
    market = Market(data)
    market.register_agent("random", 10000)
    market.register_agent("qlearner", 10000)

    agents = {
        "random":RandomAgent("random", stock_list),
        "qlearner":QLearningAgent("qlearner", stock_list, alpha = 1, epsilon = 1)
    }

    if os.path.exists("data/q_table.pkl"):
        tools.load_q_table(agents["qlearner"], "data/q_table.pkl")
        print(f"Q-table loaded with {len(agents['qlearner'].q_table)} states.")


    while market.current_step < len(data) - 1:
        state = market.get_state()
        for name, agent in agents.items():
            action = agent.act(state)
            old_value = market.get_agent_value(name)

            market.step(name, action)
            new_value = market.get_agent_value(name)
            reward = new_value - old_value

            if hasattr(agent, "update"):
                agent.update(reward, market.get_state())
                epsilon = max(0.01, agent.epsilon * 0.98)
                agent.epsilon = epsilon
                agent.alpha = max(0.05, agent.alpha * 0.95)

        
        market.next()

    for name in agents:
        history = market.get_history(name)
        final_value = history[-1]["value"]
        print(f"{name} final portfolio value: ${final_value:.2f}")
        
    tools.plot_results(market, agents)

    tools.save_q_table(agents["qlearner"], "data/q_table.pkl")
    print(f"Q-table now has {len(agents['qlearner'].q_table)} states after training.")




if __name__ == "__main__":
    main() 