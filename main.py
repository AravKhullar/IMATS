from market import Market
from agents.random_agent import RandomAgent
from agents.q_learning_agent import QLearningAgent
import tools
import os
import warnings
import pandas as pd
warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_news_sentiment(ticker: str, date) -> int:
    try:
        formatted_date = pd.to_datetime(date).strftime("%Y-%m-%d")
        news = tools.search.run(f"{ticker} stock news {formatted_date}")
        summary = tools.summarize_news(news)
        sentiment = tools.llm_sentiment(summary)

        return sentiment
    except Exception as e:
        print(f"[Sentiment Error for {ticker}] {e}")
        return 0

def main():
    data = tools.load_stock_data("data/stock_prices.csv")
    stock_list = [col for col in data.columns if col != "Date"]

    sentiment_map = {}
    
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
        if market.current_step % 300 == 0:
            for stock in stock_list:
                sentiment_map[stock] = get_news_sentiment(stock, state["date"])

        for name, agent in agents.items():
            action = agent.act(state)
            state["sentiment"] = sentiment_map.get(action["stock"], 0)
            old_value = market.get_agent_value(name)

            market.step(name, action)
            new_value = market.get_agent_value(name)
            reward = new_value - old_value

            if hasattr(agent, "update"):
                agent.update(reward, state)
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