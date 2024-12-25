import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_pnls(fp):
    trades = pd.read_csv(fp)
    if 'PnL' not in trades.columns:
        raise ValueError("The file must contain a 'PnL' column.")
    return trades['PnL'].values

def cum_ret(pnl):
    return np.cumsum(pnl)

def max_dd(cum_ret):
    peak = np.maximum.accumulate(cum_ret)
    return (cum_ret - peak).min()

def sharpe(pnl, rf=0.0):
    excess = pnl - rf
    return np.mean(excess) / np.std(excess)

def sortino(pnl, rf=0.0):
    excess = pnl - rf
    downside_dev = np.std(excess[excess < 0])
    return np.mean(excess) / downside_dev

def run_sims(pnl, n_sims=1000):
    metrics = {'max_dd': [], 'sharpe': [], 'sortino': []}
    for _ in range(n_sims):
        rand_pnl = np.random.choice(pnl, size=len(pnl), replace=True)
        cum_ret_vals = cum_ret(rand_pnl)
        metrics['max_dd'].append(max_dd(cum_ret_vals))
        metrics['sharpe'].append(sharpe(rand_pnl))
        metrics['sortino'].append(sortino(rand_pnl))
    return metrics

def plot_sims(pnl, n_sims=1000):
    plt.figure(figsize=(14,7))
    for _ in range(n_sims):
        rand_pnl = np.random.choice(pnl, size=len(pnl), replace=True)
        cum_ret_vals = cum_ret(rand_pnl)
        plt.plot(cum_ret_vals, color='blue', alpha=0.05)
    orig_cum_ret = cum_ret(pnl)
    plt.plot(orig_cum_ret, color='black', linewidth=1.5, label='Original Equity Curve')
    plt.title('Monte Carlo Simulation of Cumulative Portfolio Returns')
    plt.xlabel('Trade Index')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.show()

def print_pcts(metrics):
    for metric, values in metrics.items():
        p5, p95 = np.percentile(values, [5, 95])
        print(f"5th Percentile of {metric.capitalize()}: {p5:.4f}")
        print(f"95th Percentile of {metric.capitalize()}: {p95:.4f}")

def mc_simulation(fp, n_sims=1000, rf=0.0):
    pnl = load_pnls(fp)
    metrics = run_sims(pnl, n_sims)
    avg_max_dd = np.mean(metrics['max_dd'])
    avg_sharpe = np.mean(metrics['sharpe'])
    avg_sortino = np.mean(metrics['sortino'])
    
    print_pcts(metrics)
    plot_sims(pnl, n_sims)
    
    final_cum_ret_pct(metrics, pnl, n_sims)
    
    print(f"Avg Max Drawdown: {avg_max_dd:.4f}")
    print(f"Avg Sharpe Ratio: {avg_sharpe:.4f}")
    print(f"Avg Sortino Ratio: {avg_sortino:.4f}")

def final_cum_ret_pct(metrics, pnl, n_sims=1000):
    final_cum_ret_vals = []
    for _ in range(n_sims):
        rand_pnl = np.random.choice(pnl, size=len(pnl), replace=True)
        cum_ret_vals = cum_ret(rand_pnl)
        final_cum_ret_vals.append(cum_ret_vals[-1])
    
    pcts = np.percentile(final_cum_ret_vals, np.linspace(0, 100, 101))
    plt.figure(figsize=(14,7))
    plt.plot(np.linspace(0, 100, 101), pcts, color='blue', linewidth=2)
    plt.title('Final Cumulative Returns vs Percentile')
    plt.xlabel('Percentile')
    plt.ylabel('Final Cumulative Return')
    plt.grid(True)
    plt.show()

mc_simulation('Trades.csv')
