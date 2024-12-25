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

def max_drawdown(cum_returns):
    peak = np.maximum.accumulate(cum_returns)
    return (cum_returns - peak).min()

def sharpe_ratio(pnl_values, rf_rate=0.0):
    excess_returns = pnl_values - rf_rate
    return np.mean(excess_returns) / np.std(excess_returns)

def sortino_ratio(pnl_values, rf_rate=0.0):
    excess_returns = pnl_values - rf_rate
    downside_deviation = np.std(excess_returns[excess_returns < 0])
    return np.mean(excess_returns) / downside_deviation

def run_simulations(pnl_values, num_simulations=1000):
    metrics = {'max_drawdowns': [], 'sharpe_ratios': [], 'sortino_ratios': []}
    for _ in range(num_simulations):
        shuffled_pnl = np.random.permutation(pnl_values)
        cumulative_returns = cum_returns(shuffled_pnl)
        metrics['max_drawdowns'].append(max_drawdown(cumulative_returns))
        metrics['sharpe_ratios'].append(sharpe_ratio(shuffled_pnl))
        metrics['sortino_ratios'].append(sortino_ratio(shuffled_pnl))
    return metrics

def plot_simulations(pnl_values, num_simulations=1000):
    plt.figure(figsize=(14, 7))
    for _ in range(num_simulations):
        shuffled_pnl = np.random.permutation(pnl_values)
        cumulative_returns = cum_returns(shuffled_pnl)
        plt.plot(cumulative_returns, color='blue', alpha=0.05)
    original_cumulative_returns = cum_returns(pnl_values)
    plt.plot(original_cumulative_returns, color='black', linewidth=1.5, label='Original Equity Curve')
    plt.title('Monte Carlo Simulation of Cumulative Portfolio Returns (Resampled)')
    plt.xlabel('Trade Index')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.show()

def print_percentiles(metrics):
    for metric, values in metrics.items():
        p5, p95 = np.percentile(values, [5, 95])
        print(f"5th Percentile of {metric.capitalize()}: {p5:.4f}")
        print(f"95th Percentile of {metric.capitalize()}: {p95:.4f}")

def monte_carlo_simulation(file_path, num_simulations=1000, rf_rate=0.0):
    pnl_values = load_pnls(file_path)
    metrics = run_simulations(pnl_values, num_simulations)
    avg_max_dd = np.mean(metrics['max_drawdowns'])
    avg_sharpe = np.mean(metrics['sharpe_ratios'])
    avg_sortino = np.mean(metrics['sortino_ratios'])
    
    print_percentiles(metrics)
    plot_simulations(pnl_values, num_simulations)
    
    print(f"Average Maximum Drawdown: {avg_max_dd:.4f}")
    print(f"Average Sharpe Ratio: {avg_sharpe:.4f}")
    print(f"Average Sortino Ratio: {avg_sortino:.4f}")

monte_carlo_simulation('Trades.csv')
