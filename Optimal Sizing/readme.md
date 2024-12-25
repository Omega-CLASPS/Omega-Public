# Table of Contents
1. Introduction
2. Monte Carlo Simulation
3. Kelly Criterion
4. Combination
5. Conclusion

# 1. Introduction

This study seeks to optimize position sizing based on the 2024 results of my discretionary swing trading. In 2024, I took 59 trades and had a final adjusted cumulative return of 23.71%. My real cumulative return was higher due to aggressive sizing, but it's important to normalize the results to confirm the presence of an edge and continue to be as well-positioned as possible for future trades.

My portfolio had the following performance metrics:
1. Maximum drawdown: -3.22%
2. Sharpe Ratio: 0.286
3. Sortino Ratio: 0.955

The Sharpe ratio is so low because it punishes upside volatility, and I had a very fat right tail this year (a few big trades made up the bulk of my wins). These ratios assume a risk free rate of zero. This initial analysis can be found in Original.py.

![image](https://github.com/user-attachments/assets/48078650-dffd-4f7c-ae8d-9beaaf662454)

![image](https://github.com/user-attachments/assets/c8de6927-b713-4d23-8faf-7c1dc3ae5386)

I want to determine the optimal position sizing for swing trades I take in the future. I have previously performed iterative Kelly Cruve analysis via Excel, but I want to go more in depth for my sizing going into next year. Specifically, I want to construct a simple calculator in which I can input each new trade result and receive an updated optimal sizing. 

Anyone can use these codes with their own trade data so long as it follows the coded format. The trades should be in a .csv file with a trade indexing column called "Trade" and a PnL column called "PnL." This PnL can be percent, fraction, or currency and all codes will function the same. However, the axis/chart titles will not be accurate if the PnL is not in fraction format. 

![image](https://github.com/user-attachments/assets/a49185b4-85c2-4e88-82cf-088b64af803c)

Note that as more trades are present in the data, some of the codes will take longer to run. I've negated most of these potential effects by controlling for a simulation size that's independent of the data itself. More data tends to result in a more accurate model, but there are some key assumptions that are unrealistic. These are discussed in more detail in the study.

In this study, I will analyze the following:
1. Monte Carlo Simulation
2. Kelly Criterion
3. Combination of 1 and 2

# 2. Monte Carlo Simulation

[Build Alpha](https://www.buildalpha.com/monte-carlo-simulation/) has a good article explaining Monte Carlo simulations. There are two main simulation styles that I will run in this study:
1. Resample: Reshuffle the historical trade order N times creating N new equity curves, each with the same ending PnL. 
2. Randomize: Continuously and randomly select a historical trade with equal chance from all the trades until reaching the backtest’s trade count. Not all simulations end at the same PnL.

The codes for these two methods can be found under Resample.py and Randomize.py. Each of the codes run 1,000 simulations. Considering the low number of trades, I feel this is sufficient. 

**Resample**

![image](https://github.com/user-attachments/assets/243e6328-9582-47f3-bc31-dae84bab699a)

The Sharpe and Sortino ratios are independent of trade order and are therefore identical for all simulations. The 95th percentile MDD was -4.96%, while the 5th percentile MDD was -2.28%.

**Randomize**

![image](https://github.com/user-attachments/assets/814fde17-a168-4f98-8671-32328fede569)

![image](https://github.com/user-attachments/assets/5bc84bbc-8661-4eb1-9492-394de4938d92)

**Randomization Metrics** 

Average:
1. Maximum drawdown: -3.24%
2. Sharpe Ratio: 0.285
3. Sortino Ratio: 1.294

5th Percentile:
1. Maximum drawdown: -6.11%
2. Sharpe Ratio: 0.120
3. Sortino Ratio: 0.271

95th Percentile:
1. Maximum drawdown: -1.34%
2. Sharpe Ratio: 0.430
3. Sortino Ratio: 3.21

**Analysis**

Based on these metrics, it seems like I slightly underperformed an "average portfolio" of my trades. My max drawdown and Sharpe Ratio were near the average, but my Sortino ratio was significantly lower, likely due to the one large negative trade that was not present in a lot of simulated portfolios. The fact that the simulation results were positive until the ~3rd percentile confirms the presence of an edge for me.

The randomization simulation makes a couple of unrealistic assumptions:
1. Each trade outcome has an equal probability of happening (1 in 59) - trades are often dependent on market conditions. I'm trading U.S. equities, which tend to have some positive beta with SPX. My single biggest trade this year was GBTC into and after the 2024 U.S. election, which is a unique event that occurs once every four years.
2. Each trade is independent of the last - a lot of my large winners were flips when a trade was stopped out, which can be seen by the equity curve; a big win was often preceded by a loss. 

Regardless of these assumptions, I think this is still a decent model for a discretionary system and the removal of large outliers (percentile analysis) gives an accurate estimate of performance metrics. This approach will be used alongside the Kelly Criterion in the Combination portion of this study. 

# 3. Kelly Criterion

[The Quant Trading Room](https://medium.com/@The-Quant-Trading-Room/the-ultimate-trading-strategy-how-to-combine-kelly-criteria-and-monte-carlo-simulation-d9ce8cc2c2bc) has a good article on using a Kelly Criterion and Monte Carlo simulations to determine optimal position sizing. While the article's approach and goals are a little different from mine, the fundamentals are the same. Specifically, the article highlights two popular methods for calculating the Kelly Criterion.

**Betting Method** 

This Kelly Criterion function is mainly used for gambling, where the potential win and loss are known in advance, and the probability of a win is known or approximated. It is derived from a growth rate equation. 

$$R = (1 + bf)^p \cdot (1 - af)^q$$

$$\ln(R) = p \ln(1 + bf) + q \ln(1 - af)$$

$$\frac{d}{df} \ln(R) = \frac{d}{df} \Big( p \ln(1 + bf) + q \ln(1 - af) \Big)$$

$$\frac{1}{R} \frac{dR}{df} = p \frac{b}{1 + bf} - q \frac{a}{1 - af}$$

Setting this equal to zero yields the final equation:  

$$f = \frac{p}{a} - \frac{q}{b}$$

where:
1. *f* = Amount to trade (NOT amount to lose)
2. *p* = Probability of win
3. *a* = Loss: Amount of portfolio lost if a trade is a loser
4. *q* = Probability of loss = 1 - p
5. *b* = Payout: Amount of portfolio gained if a trade is a winner

I constructed this in Python by assuming p/q are fixed as the total WR of the portfolio. 

![image](https://github.com/user-attachments/assets/f22acf53-479e-44e5-ae4d-4eb468fbf795)

Zoomed in to my average a of 0.38% results in an extremely high f of ~80.

![image](https://github.com/user-attachments/assets/353932a4-696e-4de2-92f5-437f6897f6b9)

This is interpreted as if I were to risk 0.38% of my portfolio per trade, I should use 80x margin because my original results were very profitable. In other words, I should be willing to lose 30.4% of my portfolio per trade. This aligns with the initial iterative method I performed in Excel earlier this year, which gives an updated optimal portfolio risk of 33.0%. I chose not to cover this method in this study, but its code can be found in K1.py. 

![image](https://github.com/user-attachments/assets/5aead6d9-d7c0-4752-b363-71d6b6140349)

This is a very aggressive (and unrealistic) result - it moreso serves as a proof of concept that the traditional betting method is not appropriate for markets. It is impossible to estimate the chance of a win for my discretionary trading, and knowing a potential win size is even less realistic. The code for this method can be found in Betting Method.py.

**Thorp Method**

Edward Thorp created a new Kelly Criterion model in 1992 specifically for the stock market. 

$$f^* = \frac{\mu - r}{\sigma^2}$$

where:
1. *f** = Amount to trade (NOT amount to lose)
2. *μ* = Mean returns
3. *r* = Risk-free rate
4. *σ* = Standard deviation of returns

As long as mean returns are greater than the risk-free rate, the strategy will have a positive bet size. I will assume the risk-free rate is zero. This method punishes upside volatility, but I will run it anyways to see the results. Since this is a single equation with no variable, there is not a corresponding plot. The code can be found in Thorp Method.py.

The optimal Kelly Criterion was found to be 20.39, which corresponds to losing 7.75% of my portfolio per trade. This is much more reasonable and I will use this method when performing future Monte Carlo simulations on Kelly Criterion risk sizes.

A major weakness of this Kelly Criterion approach is that it assumes a symmetric probability density function for returns. Since I have a fat right tail, this results in an underestimate of optimal bet size. I am okay with this because I will test a wide range of bet sizes in the Combination section of this study.

# 4. Combination

The final portion of this optimization combines the Monte Carlo simulations and Kelly Criterion calculations to determine the optimal risk sizing for my swing portfolio.

My approach was to create a multi-loop simulation that steps between two ranges of the optimal Thorp Kelly Fraction (0.01 to 2.5) and runs a randomization Monte Carlo simulation for each stepped Kelly Fraction. The code then calculates the relevant metrics for the medians of each step's simulated results. I chose the median for metric analysis because there are incredibly large outliers that make the mean script's outputs messy and difficult to read. 

This code can become very computer intensive if the parameters are inappropriately increased. For a quick intensity analysis, simply multiply kelly_steps, num_simulations, and run_size together to calculate the total number of "simulations". The following results were run on 100, 100,000, 150 which results in 1.5 billion "simulations". This took my laptop 633 seconds to run. 

![image](https://github.com/user-attachments/assets/f957618d-aee5-41b9-a1c8-3a91e109ca1c)

![image](https://github.com/user-attachments/assets/474c352a-5c1b-4825-bab6-7bcc06006166)

With a Van Thorp risk size that is 0.68 of the optimal combination risk size, the simulation had an 81% reduction in median return and a 96% reduction in variance. 

The ruin rate is the rate at which simulated portfolios dropped below their maximum value to a threshold of a maximum value. As an example, consider a portfolio with a threshold of .75. If the portfolio went from $1 to $10, then dropped down to $7.50, it would be considered ruined. If the portfolio went straight from $1 to $0.75, it would also be ruined. Another way to think of the threshold is as a maximum allowable drawdown equal to 1 - threshold.

For me, an account is ruined if it loses 75% of its value - this corresponds to a threshold of 0.25. The ruin rate is also dependent on the run size, since more trades result in a greater likelihood of ruin. I treat this as a worst-case analysis which shows the probability of a massive drawdown ocurring. Note I also tested a ruin definition that was dependent only on the starting and ending portfolio value, but that was a horizontal line at zero until my threshold began to reach 0.9 since it is extremely likely that a simulated portfolio will end in profit.

Having a run size of 150 means 150 trades were taken in each portfolio. To simulate this year, I would do a run size of 59, but this would result in a lower risk of ruin and I want to base my sizing on a more unfavorable model to (hopefully) counteract any positive effects from the previously discussed unrealistic assumptions. 

The code for this section can be found in Combination.py.

# 5. Conclusion

In this study I performed analysis based on Monte Carlo simulations and the Kelly Criterion. Along the way, I constructed codes that can be used with anayone's trade data to give them a custom sizing recommendation.

I received an optimal Thorp risk size of 7.75% which corresponds to a roughly 30% risk of ruin (75% drawdown) in the event of a doubling in trade frequency. I believe I've controlled and adjusted for assumptions as much as possible, but this is still more risk than I'm comfortable taking. Therefore my risk size will be 5%, which is still on the aggressive side for a typical trader's risk profile.
