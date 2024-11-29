import pandas as pd
import matplotlib.pyplot as plt

def create_df(ticker, folder_path="hist csv", period=14, lower_threshold=30, upper_threshold=70):
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

def plot_ret(df, ticker):
    df["Date"] = pd.to_datetime(df["Date"])
    plt.figure(figsize=(14, 7))
    plt.plot(df["Date"], df["Cumul Ret"], label=f"Strategy", color="blue")
    plt.plot(df["Date"], df[f"Cumul {ticker} Ret"], label=ticker, color="orange")
    plt.title(f"Cumulative Returns: Strategy vs {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_dd(df, ticker):
    df["CumTotalDD"] = ((df["Cumul Ret"] + 1) - (df["Cumul Ret"] + 1).cummax()) / (df["Cumul Ret"] + 1).cummax()
    df[f"Cum{ticker}DD"] = ((df[f"Cumul {ticker} Ret"] + 1) - (df[f"Cumul {ticker} Ret"] + 1).cummax()) / (df[f"Cumul {ticker} Ret"] + 1).cummax()
    
    plt.figure(figsize=(14, 7))
    plt.plot(df["Date"], df["CumTotalDD"], label="Strategy ", color="blue")
    plt.plot(df["Date"], df[f"Cum{ticker}DD"], label=f"{ticker}", color="orange")
    plt.title(f"Cumulative Drawdowns: Strategy vs {ticker}")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Drawdown")
    plt.legend()
    plt.grid(True)
    plt.show()

def print_num_trades(df):
    num_trades = ((df["Signal"] == 1) & (df["Signal"].shift(1) == 0)).sum()
    print(f"Number of trades entered: {num_trades}")


ticker = "QQQ"
lbPeriod = 3
lThresh = 15
uThresh = 70
df = create_df(ticker, period=lbPeriod, lower_threshold=lThresh, upper_threshold=uThresh)

plot_ret(df, ticker)
plot_dd(df, ticker)
print_num_trades(df)
