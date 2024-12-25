import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_pnls(file_path):
    trades = pd.read_csv(file_path)
    if 'PnL' not in trades.columns:
        raise ValueError("The file must contain a 'PnL' column.")
    return trades['PnL'].values

def calc_probs(pnl_values):
    total_trades = len(pnl_values)
    wins = len(pnl_values[pnl_values > 0])
    losses = total_trades - wins
    return wins / total_trades, losses / total_trades

def calc_b(pnl_values):
    wins = pnl_values[pnl_values > 0]
    return np.mean(wins) if len(wins) > 0 else 0

def avg_loss(pnl_values):
    losses = pnl_values[pnl_values < 0]
    return np.abs(np.mean(losses)) if len(losses) > 0 else 0

def kelly(p, q, b, a_values):
    return [(p / a - q / b) if a > 0 else np.nan for a in a_values]

def plot_kelly(a_values, f_values):
    plt.figure(figsize=(14,7))
    plt.plot(a_values, f_values, label="Kelly Curve", color='blue')
    plt.title('Kelly Curve: f vs a')
    plt.xlabel('Amount Lost per Trade (a)')
    plt.ylabel('Optimal Fraction (f)')
    plt.grid(True)
    plt.legend()
    plt.show()

def analyze(file_path):
    pnl_values = load_pnls(file_path)
    p, q = calc_probs(pnl_values)
    b = calc_b(pnl_values)
    avg_loss_value = avg_loss(pnl_values)
    print(f"Average Loss (a): {avg_loss_value:.4f}")
    a_values = np.linspace(0.00, .2, 100)
    f_values = kelly(p, q, b, a_values)
    plot_kelly(a_values, f_values)

analyze('Trades.csv')
