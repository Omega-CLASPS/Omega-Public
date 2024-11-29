import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import create_df function
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

def calculateSharpes(ticker="QQQ", folder_path="hist csv", period=3, lower_start=5, lower_end=50, upper_start=55, upper_end=95):
    results = []
    
    for lower_threshold in range(lower_start, lower_end + 1):
        row = []
        for upper_threshold in range(upper_start, upper_end + 1):
            df = create_df(ticker, folder_path, period, lower_threshold, upper_threshold)
            daily_returns = df["Ret"]
            sharpe_ratio = np.sqrt(252) * daily_returns.mean() / daily_returns.std()
            row.append(sharpe_ratio)
        results.append(row)
    
    sharpe_matrix = pd.DataFrame(results, index=range(lower_start, lower_end + 1), columns=range(upper_start, upper_end + 1))
    return sharpe_matrix

def plotHeatmap(ticker="QQQ", folder_path="hist csv", period=3, lower_start=5, lower_end=50, upper_start=55, upper_end=95):
    sharpe_matrix = calculateSharpes(ticker, folder_path, period, lower_start, lower_end, upper_start, upper_end)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(sharpe_matrix, annot=False, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Sharpe Ratio'})
    plt.title(f"Sharpe Ratios for {ticker} Across Threshold Combinations \n Lookback Period: {period}")
    plt.xlabel("Upper Threshold")
    plt.ylabel("Lower Threshold")
    plt.xticks(rotation=45)
    plt.show()

plotHeatmap()
