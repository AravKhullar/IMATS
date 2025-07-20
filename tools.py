import pandas as pd
import matplotlib.pyplot as plt
import pickle

def load_stock_data(path: str):
    df = pd.read_csv(path)
    if "Date" in df.columns:
        df = df.drop(columns = "Date")
    return df

def calculate_portfolio_value(cash: float, shares: dict, prices: dict):
    value = cash
    for stock, amount in shares.items():
        value += amount * prices.get(stock, 0)
    return value

def plot_results(market, agents):
    plt.figure(figsize=(10, 5))
    for name in agents:
        history = market.get_history(name)
        values = [entry["value"] for entry in history]
        steps = [entry["step"] for entry in history]
        plt.plot(steps, values, label = name)
    
    plt.title("Agent Portfolio Value Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def save_q_table(agent, filename):
    with open(filename, "wb") as f:
        pickle.dump(agent.q_table, f)

def load_q_table(agent, filename):
    with open(filename, "rb") as f:
        agent.q_table = pickle.load(f)