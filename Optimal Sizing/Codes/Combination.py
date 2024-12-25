import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    trades = pd.read_csv(file_path)
    if 'PnL' not in trades.columns:
        raise ValueError("The file must contain a 'PnL' column.")
    return trades['PnL'].values

def calc_thorp_kelly(mu, sigma_sq, rf_rate):
    return (mu - rf_rate) / sigma_sq

def calc_stats(pnl_values):
    mu = np.mean(pnl_values)
    sigma_sq = np.var(pnl_values)
    avg_loss = np.mean(pnl_values[pnl_values < 0])
    return mu, sigma_sq, avg_loss

def monte_carlo(file_path, rf_rate, kelly_steps, sims, size=100):
    pnl_values = load_data(file_path)
    mu, sigma_sq, avg_loss = calc_stats(pnl_values)
    opt_kelly = calc_thorp_kelly(mu, sigma_sq, rf_rate)
    
    kelly_fractions = np.linspace(0.01, 2.5, kelly_steps) * opt_kelly
    amount_risked = kelly_fractions * abs(avg_loss) * 100
    
    median_returns = []
    median_vars = []
    for kelly_frac in kelly_fractions:
        final_returns = []
        variances = []
        for _ in range(sims):
            portfolio_values = []
            portfolio = 1
            pnl_sim = np.random.choice(pnl_values, size=size, replace=True)
            for pnl in pnl_sim:
                portfolio *= 1 + kelly_frac * pnl
                if portfolio <= 0:
                    portfolio = 0
                    break
                portfolio_values.append(portfolio)
            if portfolio_values:
                final_returns.append(portfolio)
                variances.append(np.var(portfolio_values))
            else:
                final_returns.append(0)
                variances.append(0)
        median_returns.append(np.median(final_returns))
        median_vars.append(np.median(variances))
    
    return amount_risked, median_returns, median_vars, mu, sigma_sq, avg_loss

def plot_data(file_path, rf_rate, amount_risked, median_returns, median_vars, ruin_rates, threshold):
    pnl_values = load_data(file_path)
    mu, sigma_sq, avg_loss = calc_stats(pnl_values)
    opt_kelly_risk = calc_thorp_kelly(mu, sigma_sq, rf_rate) * abs(avg_loss) * 100
    
    max_return = max(median_returns)
    max_variance = max(median_vars)
    
    norm_returns = [r / max_return for r in median_returns]
    norm_vars = [v / max_variance for v in median_vars]

    max_return_idx = np.argmax(median_returns)
    max_return_risk = amount_risked[max_return_idx]
    
    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(amount_risked, norm_vars, label='Normalized Median Variance', color='orange')
    ax.plot(amount_risked, norm_returns, label='Normalized Median Return', color='blue')
    ax.plot(amount_risked, ruin_rates, label=f'Ruin Rate (Threshold {threshold})', color='red')
    ax.axvline(x=opt_kelly_risk, color='green', linestyle='--', label='Optimal Van Thorp Risk Size')
    ax.axvline(x=max_return_risk, color='purple', linestyle='--', label='Maximum Median Return')
    
    ax.set_xlabel('Amount Risked per Trade (%)')
    ax.set_ylabel('Normalized Metric (Fraction of Max)')
    ax.set_title('Simulation: Normalized Metrics vs Risk Size')
    ax.grid(True)
    ax.legend(loc="upper left")

    plt.show()

def risk_size_ratio(file_path, rf_rate, amount_risked, median_returns, median_vars):
    pnl_values = load_data(file_path)
    mu, sigma_sq, avg_loss = calc_stats(pnl_values)
    
    van_thorp_kelly = calc_thorp_kelly(mu, sigma_sq, rf_rate)
    van_thorp_risk_size = van_thorp_kelly * abs(avg_loss) * 100
    
    max_return_idx = np.argmax(median_returns)
    opt_risk_size = amount_risked[max_return_idx]
    
    opt_median_return = median_returns[max_return_idx]
    opt_median_variance = median_vars[max_return_idx]
    
    van_thorp_median_return = median_returns[np.argmin(np.abs(amount_risked - van_thorp_risk_size))]
    van_thorp_median_variance = median_vars[np.argmin(np.abs(amount_risked - van_thorp_risk_size))]
    
    ratio_return = van_thorp_median_return / opt_median_return
    ratio_variance = van_thorp_median_variance / opt_median_variance
    ratio_risk_size = van_thorp_risk_size / opt_risk_size
    
    print(f"Van Thorp Risk Size: {van_thorp_risk_size:.2f}%")
    print(f"Opt Risk Size: {opt_risk_size:.2f}%")
    print(f"Ratio of Van Thorp Risk Size to Optimal Risk Size: {ratio_risk_size:.2f}")
    print(f"Ratio of Van Thorp Median Return to Optimal Median Return: {ratio_return:.2f}")
    print(f"Ratio of Van Thorp Median Variance to Optimal Median Variance: {ratio_variance:.2f}")

def plot_ruin_rate(file_path, rf_rate, amount_risked, median_returns, kelly_steps, sims, size=100, threshold=0.75):
    pnl_values = load_data(file_path)
    mu, sigma_sq, avg_loss = calc_stats(pnl_values)
    
    ruin_rates = []
    
    for kelly_frac in np.linspace(0.01, 2.5, kelly_steps) * calc_thorp_kelly(mu, sigma_sq, rf_rate):
        ruin_count = 0
        for _ in range(sims):
            portfolio = 1
            pnl_sim = np.random.choice(pnl_values, size=size, replace=True)
            portfolio_values = []
            max_value = 1
            
            for pnl in pnl_sim:
                portfolio *= 1 + kelly_frac * pnl
                max_value = max(max_value, portfolio)
                portfolio_values.append(portfolio)
                
                if portfolio <= threshold * max_value:
                    ruin_count += 1
                    break
            
        ruin_rate = ruin_count / sims
        ruin_rates.append(ruin_rate)
    
    return ruin_rates

file_path = 'Trades.csv'
rf_rate = 0
kelly_steps = 100
num_simulations = 100000
run_size = 150
threshold = 0.25

amount_risked, median_returns, median_vars, mu, sigma_sq, avg_loss = monte_carlo(
    file_path, rf_rate, kelly_steps, num_simulations, size = run_size
)

ruin_rates = plot_ruin_rate(file_path, rf_rate, amount_risked, median_returns, kelly_steps, num_simulations, size=run_size, threshold=threshold)

plot_data(file_path, rf_rate, amount_risked, median_returns, median_vars, ruin_rates, threshold)
risk_size_ratio(file_path, rf_rate, amount_risked, median_returns, median_vars)
