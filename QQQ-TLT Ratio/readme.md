# Introduction
This is a Python conversion of the NQ ZB Ratio Strategy from NinjaTrader. Instead of comparing NQ (or ES) and ZB futures, this code compares QQQ (or SPY) and TLT. 

The data is tested from TLT inception (7-30-2022) to present (11-25-2024).

To reiterate, these are the strategy rules:
1. We make a "spread" of QQQ and TLT. This is simply the price of QQQ divided by TLT.
2. We make a 3-day RSI of the spread in number 1.
3. When the value in number 2 (the RSI of the spread) is below 15, we go long QQQ. We cover when the RSI rises above 70.

The default parameter settings are: 
1. Lookback Period = 3
2. Lower Threshold = 15
3. Upper Threshold = 70

Because this strategy has three parameters, I don't plan to incorporate this into my portfolio. This is moreso a hybrid between an edge verification and an initial strategy analysis rather than a traditional first step.

I want to "optimize" for the most reliable settings without simply picking the best combination. I instead want to see parameter ranges/areas that consistently provide better performance. This will also serve as a robustness test. I decided to optimize for Sharpe ratio.

# Optimization
I began optimization with a visual representation of the effect of strategy parameters on Sharpe Ratios. I did this by coding one-dimensional loops with the other two parameters set to their defaults:

![image](https://github.com/user-attachments/assets/f4e7f996-85f5-4aa7-81fd-c1da2dbccd13)

![image](https://github.com/user-attachments/assets/c4028b2a-0790-4012-a364-720c465246b8)

![image](https://github.com/user-attachments/assets/969a8c4b-bd4a-41dd-b085-ca0524c25ac5)

The codes for these one-dimensional plots are in "L Opt.py" (Lower Threshold), "U Opt.py" (Upper Threshold), and "LB Opt.py" (Lookback Period).

After confirming that the lookback period was effectively fixed at 3 days, I used Seaborn to generate a heatmap of threshold combinations. The goal was not necessarily to pick the best pair, but instead to observe the "hot" and "cold" areas to see if the edge is consistent in different parameter locations. It certainly looks the way I wanted it to. 

![image](https://github.com/user-attachments/assets/f94f1785-352b-4ed6-b4a7-d715384e8159)

The code for this heatmap can be found in "Heatmap.py". Note that this code is CPU-intensive; it took my laptop 20 minutes to run through the 1,800 combinations!

# Discussion
This served as a good initial robustness test and optimization of the QQQ-TLT ratio strategy. I confirmed that a 3-day lookback period is the best parameter choice and was able to find a range of optimal threshold levels for 22 years of historical data. The lower threshold is best between 20 and 30, while the upper threshold is best between 65 and 70. Performance begins to break down once the lower threshold exceeds ~35 and the upper threshold exceeds ~80. 

I would not feel comfortable giving this strategy a lot of weight in my portfolio if I ever chose to run it. Not only are trades relatively infrequent, but the strategy requires 3 parameters. I could maybe treat the lookback period as half a parameter and justify it as a direct reflection of the market's quick response to the relationship between equities and bonds, but this is spotty logic at best. I would rather treat this effect as a proxy to a post-signal information coefficient.

The one-dimensional test confirms that a shorter lookback period performs better, so I cannot use my traditional 252D Z-score approach without adding two (half-)parameters anyways: upper and lower Z-score thresholds.

That being said, I definitely think there is some potential here. My goal is to find a one-parameter, non-indicator-based method to measure the short-term relationship between equities and bonds. Depending on how I decide to treat the lookback period, I would then be able to create a 1.5- or 2-parameter strategy that captures the same idea with more statistical significance at the price of worsening performance. 

**Verdict: Inconclusive.** 

Some potential, but inclusion into the portfolio is dependent on discovering a different method than RSI to define short-term relationships between equities and bonds.

# Plots
The code for plot generation can be found in "Plots.py". A trade is only when a buy is activated (previous day signal = 0, current day signal = 1).

Original strategy parameters: 3-day lookback, lower threshold = 15, upper threshold = 70. N Trades = 381.

![image](https://github.com/user-attachments/assets/45fca4cf-cfec-4498-8d0f-36052272a722)

![image](https://github.com/user-attachments/assets/c078271b-bcd5-47bc-96cf-914ece71f20a)

Optimal strategy parameters: 3-day lookback, lower threshold = 25, upper threshold = 68. N Trades = 464.

![image](https://github.com/user-attachments/assets/82086550-0b73-4ee0-bf69-2e38c66f3a78)

![image](https://github.com/user-attachments/assets/6f2f448b-df9c-4bff-8558-9e274bb0d451)
