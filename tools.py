import pandas as pd
import matplotlib.pyplot as plt
import pickle
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def load_stock_data(path: str):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
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

search = DuckDuckGoSearchRun()

search_tool = Tool(
    name = "news_search",
    func = search.run,
    description="Use this to search for the latest news about a stock or company. Input should be the company name or stock ticker.",
)

llm = ChatOpenAI(model = "o4-mini-2025-04-16")

def summarize_news(text):
    prompt = f"Summarize this financial news content for its potential impact on stock prices:\n\n{text}"
    return llm.invoke(prompt)

summarize_tool = Tool(
    name="summarize_news",
    func=summarize_news,
    description="Summarizes financial news to assess impact on stock prices"
)

def llm_sentiment(text):
    prompt = f"Is the tone of this news positive, negative, or neutral for investors? Respond with -1, 0, or 1 only.\n\n{text}"
    response = llm.invoke(prompt)
    if hasattr(response, "content"):
        return int(str(response.content).strip())
    else:
        print("Unexpected response:", response)
        return 0

sentiment_tool = Tool(
    name="classify_sentiment",
    func=llm_sentiment,
    description="Classifies the sentiment of financial news for a stock. Output is -1, 0, or 1"
)