import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_pnls(file_path):
    trades = pd.read_csv(file_path)
    if 'PnL' not in trades.columns:
        raise ValueError("The file must contain a 'PnL' column.")
    return trades['PnL'].values

def cum_returns(pnl_values):
    return np.cumsum(pnl_values)

def final_cum_return(pnl_values):
    return np.sum(pnl_values)

def max_drawdown(cum_returns):
    peak = np.maximum.accumulate(cum_returns)
    drawdown = cum_returns - peak
    return drawdown.min()

def sharpe_ratio(pnl_values, rf_rate=0.0):
    excess_returns = pnl_values - rf_rate
    return np.mean(excess_returns) / np.std(excess_returns)

def sortino_ratio(pnl_values, rf_rate=0.0):
    excess_returns = pnl_values - rf_rate
    downside_deviation = np.std(excess_returns[excess_returns < 0])
    return np.mean(excess_returns) / downside_deviation

def plot_curve(cum_returns):
    plt.figure(figsize=(14,7))
    plt.plot(cum_returns, color='blue', linewidth=1)
    plt.title('Portfolio Equity Curve')
    plt.xlabel('Trade Index')
    plt.ylabel('Cumulative Return')
    plt.grid(True)
    plt.show()

def analyze(file_path, rf_rate=0.0):
    pnl_values = load_pnls(file_path)
    cum_returns_val = cum_returns(pnl_values)
    final_return = final_cum_return(pnl_values)
    max_dd = max_drawdown(cum_returns_val)
    sharpe = sharpe_ratio(pnl_values, rf_rate)
    sortino = sortino_ratio(pnl_values, rf_rate)
    plot_curve(cum_returns_val)
    print(f"Final Cumulative Return: {final_return:.4f}")
    print(f"Maximum Drawdown: {max_dd:.4f}")
    print(f"Sharpe Ratio: {sharpe:.4f}")
    print(f"Sortino Ratio: {sortino:.4f}")

analyze('Trades.csv')
