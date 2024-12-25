import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_pnls(file_path):
    trades = pd.read_csv(file_path)
    if 'PnL' not in trades.columns:
        raise ValueError("The file must contain a 'PnL' column.")
    return trades['PnL'].values

def thorp_kelly(mu, sigma_squared, rf_rate):
    return (mu - rf_rate) / sigma_squared

def stats(pnl_values):
    mu = np.mean(pnl_values)
    sigma_squared = np.var(pnl_values)
    sigma = np.sqrt(sigma_squared)
    return mu, sigma_squared, sigma

def analyze(file_path, rf_rate):
    pnl_values = load_pnls(file_path)
    mu, sigma_squared, sigma = stats(pnl_values)
    kelly_fraction = thorp_kelly(mu, sigma_squared, rf_rate)
    print(f"Mean PnL (µ): {mu:.4f}")
    print(f"Variance (σ²): {sigma_squared:.4f}")
    print(f"Standard Deviation (σ): {sigma:.4f}")
    print(f"Risk-Free Rate (r): {rf_rate:.4f}")
    print(f"Optimal Kelly Criterion (f): {kelly_fraction:.4f}")
    plt.figure(figsize=(14,7))
    plt.hist(pnl_values, bins=30, color='blue', alpha=0.7, label='PnL Distribution')
    plt.axvline(mu, color='red', linestyle='--', label='Mean PnL (µ)')
    plt.axvline(mu - sigma, color='orange', linestyle='--', label='1 Std Dev Below µ')
    plt.axvline(mu + sigma, color='orange', linestyle='--', label='1 Std Dev Above µ')
    plt.title('Distribution of Trade PnL')
    plt.xlabel('PnL')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()

analyze('Trades.csv', rf_rate=0)
