# Purpose
To track the relation between NQ (QQQ) and ZB (TLT). The ratio between the two is expected to mean revert; when NQ is "cheap" relative to ZB (calculated by an RSI of the ratio), buy NQ. Scale out of the NQ long when it becomes "expensive" relative to ZB. Vice versa for ZB.

# Literature
This is a strategy a friend shared with me. The rules are as follows: 
  
1. We make a "spread" of QQQ and TLT. This is simply the price of QQQ divided by TLT.
2. We make a 3-day RSI of the spread in number 1.
3. When the value in number 2 (the RSI of the spread) is below 15, we go long QQQ. We cover when the RSI rises above 70.
4. When the value in number 2 is over 85, we go long TLT. We cover when the RSI drops below 30.
5. All buying and selling are done at the close.
6. We allocate 100% of the equity to each trade.
  
# Code Breakdown 
This code is intended to be used with NQ. It calls ZB as a secondary data series and calculates the ratio and its RSI.

The strategy enters when a candle closes with a ratio below its lower threshold. It exits this long when the RSI *crosses below* its upper threshold.

Both the indicator and strategy have three changeable parameters: The RSI lookback period, the upper RSI threshold, and the lower RSI threshold. The RSI lookback period appears to be set at 3 for all intents and purposes - anything above a 5 is simply too delayed, but may prove beneficial for longer term trades.

![image](https://github.com/user-attachments/assets/7f7d466c-aae3-4194-a86c-ea5580955392)

# Review 
The indicator works as expected. It functions as a typical short-term oversold signal, which gives consistent wins when correct but large drawdowns when wrong. If used with discretion, I think this is a very powerful indicator. It is rare when the RSI reclaims a lower threshold and does not have a substantial immediate bounce.

The strategy works as expected. NinjaTrader logic dictates that when a signal is generated, the trade is taken at the open of the following candle. This means that when this strategy signals a buy at the close of a day, the long entry is taken at the open of the following day. The strategy needs to enter at the close of each signal day and may lose out on overnight gains. This issue could also protect from overnight losses. For now, the delayed daily entry is sufficient. 

Since this strategy is long only, I think it will have a positive correlation with my portfolio. However, since this is more mean reversion/"buy the dip" compared to my longer-term momentum strategies, I don't think it will be very highly correlated. 

I also need to consider that the strategy only takes between three and six trades a year. This is a low frequency strategy and it would not be optimal to allocate a large amount of portoflio capital to it. Furthermore, because of the low frequency of the trades, I cannot be confident in the strategy's robustness. This strategy would have a very small role in my portfolio, if any.

Finally, I tried a new strategy that entered long when the RSI crossed above its lower threshold, similar to the current exit system. It also used early exits when RSI crossed under its lower threshold again in the hope of minimizing drawdowns. This strategy had worse performance across the board.
![image](https://github.com/user-attachments/assets/4fe959f7-4a54-47c6-9d2c-192379635e25)

# Performance 

The following backtests/optimizations are performed from 2009 to present. 2009 is how far back my NQ data goes.

Strategy Paramaters: Lookback Period, Lower Threshold, Upper Threshold


Base strategy: 3, 15, 70
![image](https://github.com/user-attachments/assets/561c2607-74bf-45e8-ba64-2857303303c9)
![image](https://github.com/user-attachments/assets/cf9693ff-80c6-4a12-be33-98594490ad66)


Optimization for upper and lower thresholds. Optimization for lookback period consistently had 3 days as the best performer. The strategy was optimized for maximum Sortino Ratio. 

Top performer: 3, 16, 90
![image](https://github.com/user-attachments/assets/e4284990-9ee5-4c03-bb44-5b3fa9441f96)
![image](https://github.com/user-attachments/assets/32701d67-f909-4484-91d2-0b8a1e875e4c)

I noticed that all of the top 20 strategies had small lower thresholds and large upper thresholds. This may support the concept of staying in the market for as long as possible, regardless of strategy ("time in the market"). 
