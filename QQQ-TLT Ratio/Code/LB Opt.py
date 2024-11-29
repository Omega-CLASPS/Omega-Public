import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_df(ticker="QQQ", folder_path="hist csv", period=3, lower_threshold=30, upper_threshold=70):
    ticker_file = f"{folder_path}/{ticker}.csv"
    tlt_file = f"{folder_path}/TLT.csv"
    
    ticker_df = pd.read_csv(ticker_file)
    tlt_df = pd.read_csv(tlt_file)
    
    ticker_column = f"{ticker}_Adj_Close"
    ticker_data = ticker_df[["Date", "Adj Close"]].rename(columns={"Adj Close": ticker_column})
    tlt_data = tlt_df[["Date", "Adj Close"]].rename(columns={"Adj Close": "TLT_Adj_Close"})
    
    combined_df = pd.merge(ticker_data, tlt_data, on="Date")
    combined_df["Date"] = pd.to_datetime(combined_df["Date"])
    combined_df = combined_df.sort_values(by="Date")

    combined_df["ratio"] = combined_df[ticker_column] / combined_df["TLT_Adj_Close"]
    
    delta = combined_df["ratio"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    
    rs = avg_gain / avg_loss
    combined_df["RSI"] = 100 - (100 / (1 + rs))
    
    combined_df["Signal"] = 0

    signal_active = False
    for i in range(1, len(combined_df)):
        if not signal_active and combined_df.loc[i - 1, "RSI"] > lower_threshold and combined_df.loc[i, "RSI"] <= lower_threshold:
            signal_active = True
        elif signal_active and combined_df.loc[i - 1, "RSI"] < upper_threshold and combined_df.loc[i, "RSI"] >= upper_threshold:
            signal_active = False
        combined_df.loc[i, "Signal"] = int(signal_active)
    
    combined_df[f"{ticker} Ret"] = combined_df[ticker_column].pct_change()
    combined_df[f"Cumul {ticker} Ret"] = (1 + combined_df[f"{ticker} Ret"]).cumprod() - 1

    combined_df["Ret"] = combined_df[f"{ticker} Ret"] * combined_df["Signal"].shift(1)
    combined_df["Cumul Ret"] = (1 + combined_df["Ret"]).cumprod() - 1

    return combined_df

def LB_Opt(ticker="QQQ", folder_path="hist csv", lower_threshold=15, upper_threshold=70, lb_start=1, lb_end=20):
    results = []

    for period in range(lb_start, lb_end + 1):
        df = create_df(ticker, folder_path, period, lower_threshold, upper_threshold)
        daily_returns = df["Ret"]
        sharpe_ratio = np.sqrt(252) * daily_returns.mean() / daily_returns.std()
        results.append((period, sharpe_ratio))
    
    result_df = pd.DataFrame(results, columns=["Lookback Period", "Sharpe Ratio"])
    return result_df

def plotLBOpt(ticker="QQQ", folder_path="hist csv", lower_threshold=15, upper_threshold=70, lb_start=1, lb_end=20):
    result_df = LB_Opt(ticker, folder_path, lower_threshold, upper_threshold, lb_start, lb_end)

    plt.figure(figsize=(14, 7))
    plt.bar(result_df["Lookback Period"], result_df["Sharpe Ratio"], color="blue")
    plt.xlabel("Lookback Period")
    plt.ylabel("Sharpe Ratio")
    plt.title(f"Sharpe Ratios for {ticker} Across Lookback Periods \n Lower Threshold: {lower_threshold}, Upper Threshold: {upper_threshold}")
    x_ticks = np.arange(lb_start, lb_end + 1, 1)
    plt.xticks(x_ticks)
    plt.yticks()
    plt.show()

plotLBOpt()
