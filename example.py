import talib
from backtesting import Backtest, Strategy
from backtesting.test import GOOG  # Google Data
from backtesting.lib import crossover

# print(GOOG)
"""
2004-08-19  100.00  104.06   95.96  100.34  22351900
2004-08-20  101.01  109.08  100.50  108.31  11428600
2004-08-23  110.75  113.48  109.05  109.40   9137200
2004-08-24  111.24  111.60  103.57  104.87   7631300
2004-08-25  104.96  108.00  103.88  106.00   4598900
...            ...     ...     ...     ...       ...
2013-02-25  802.30  808.41  790.49  790.77   2303900
2013-02-26  795.00  795.95  784.40  790.13   2202500
2013-02-27  794.80  804.75  791.11  799.78   2026100
2013-02-28  801.10  806.99  801.03  801.20   2265800
2013-03-01  797.80  807.14  796.15  806.19   2175400

[2148 rows x 5 columns]
"""

# Optimization Metrics
def optim_func(series) -> float:
    if series['# Trades'] < 10:
        return -1
    
    return series["Equity Final [$]"] / series["Exposure Time [%]"]



class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30

    rsi_window = 14

    def init(self) -> None: # TODO FIND why only init()
        self.rsi = self.I(talib.RSI, self.data.Close, 14)  # How to build Indicators
        # RSI -> Relative Strength Index -> It takes as an argument the period in that case 14

    def next(self) -> None:  # Goes trough each candle 
        if crossover(self.rsi, self.upper_bound): # Checks if the srength index is higher than the upper bound
            self.position.close()
        elif crossover(self.lower_bound, self.rsi): # Checks if the, strength index is lower than the lower bound
            self.buy()

bt = Backtest(GOOG, RsiOscillator, cash = 10_000)
# BUILD IN BACKTEST CLASS ->  def __init__(self, data: pd.DataFrame, strategy: Type[Strategy], *, cash: float = 10_000, commission: float = .0, margin: float = 1., trade_on_close=False, hedging=False, exclusive_orders=False):

# stats = bt.optimize(
#     upper_bound = range(50, 85, 5),
#     lower_bound = range(10, 45, 5),
#     rsi_window = range(10, 30, 2),
#     maximize = 'Sharpe Ratio',
# ) # -> Searching for best of 490 configurations.
# print(stats)
# stats = bt.run() # Build in method display in CLI format

# Example with a constraint
# stats = bt.optimize(
#     upper_bound = range(10, 85, 5),
#     lower_bound = range(10, 85, 5),
#     rsi_window = range(10, 30, 2),
#     maximize = 'Sharpe Ratio',
#     constraint = lambda param: param.upper_bound > param.lower_bound 
# ) # -> Searching for best of 1050 configurations.
# print(stats)


stats = bt.optimize(
    upper_bound = range(50, 85, 5),
    lower_bound = range(10, 45, 5),
    rsi_window = range(10, 30, 2),
    maximize = optim_func,
    constraint = lambda param: param.upper_bound > param.lower_bound,
)   
print(stats)

# print(stats)
bt.plot() # filname -> https://kernc.github.io/backtesting.py/doc/backtesting/backtesting.html#gsc.tab=0

