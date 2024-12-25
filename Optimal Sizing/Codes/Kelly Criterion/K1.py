import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_pnls(file_path):
    trades = pd.read_csv(file_path)
    if 'PnL' not in trades.columns:
        raise ValueError("The file must contain a 'PnL' column.")
    return trades['PnL'].values

def win_loss_ratio(pnl_values):
    wins = pnl_values[pnl_values > 0]
    losses = pnl_values[pnl_values < 0]
    return np.inf if len(losses) == 0 else np.mean(wins) / np.abs(np.mean(losses))

def simulate(pnl_values, risk_percentage, wl_ratio, num_trades=59):
    portfolio_value = 1
    for i in range(num_trades):
        pnl = pnl_values[i]
        portfolio_value *= (1 + risk_percentage * wl_ratio) if pnl > 0 else (1 - risk_percentage)
    return portfolio_value

def plot_curve(pnl_values, wl_ratio, max_risk=1, num_simulations=100):
    risks = np.linspace(0.01, max_risk, num_simulations)
    final_returns = []
    for risk in risks:
        final_portfolio_values = [simulate(pnl_values, risk, wl_ratio) for _ in range(100)]
        final_returns.append(np.mean(final_portfolio_values))
    
    plt.figure(figsize=(14,7))
    plt.plot(risks, final_returns, label="Final Cumulative Return", color='blue')
    plt.title('Final Cumulative Return vs Risk Percentage per Trade')
    plt.xlabel('Risk Percentage per Trade')
    plt.ylabel('Average Final Portfolio Value')
    plt.grid(True)
    plt.legend()
    plt.show()

def kelly(pnl_values, wl_ratio, max_risk=1, num_simulations=100):
    risks = np.linspace(0.01, max_risk, num_simulations)
    final_returns = []
    for risk in risks:
        final_portfolio_values = [simulate(pnl_values, risk, wl_ratio) for _ in range(100)]
        final_returns.append(np.mean(final_portfolio_values))
    
    max_y_value = max(final_returns)
    max_x_value = risks[np.argmax(final_returns)]
    
    return max_x_value, final_returns, risks

def analyze(file_path):
    pnl_values = load_pnls(file_path)
    wl_ratio = win_loss_ratio(pnl_values)
    optimal_risk, final_returns, risks = kelly(pnl_values, wl_ratio)
    
    print(f"The Kelly Criterion (optimal risk per trade) is: {optimal_risk:.4f}")
    
    plt.figure(figsize=(14,7))
    plt.plot(risks, final_returns, label="Final Cumulative Return", color='blue')
    plt.title('Final Cumulative Return vs Risk per Trade')
    plt.xlabel('Risk per Trade')
    plt.ylabel('Average Final Cumulative Return')
    plt.grid(True)
    plt.legend()
    plt.show()

analyze('Trades.csv')
