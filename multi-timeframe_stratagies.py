import talib
import seaborn as sns
import matplotlib.pyplot as plt
from backtesting import Backtest, Strategy
from backtesting.test import GOOG 
from backtesting.lib import crossover, resample_apply


# Doc -> https://kernc.github.io/backtesting.py/doc/backtesting/#gsc.tab=0


def optim_func(series) -> float:
    if series['# Trades'] < 10:
        return -1
    
    return series["Equity Final [$]"] / series["Exposure Time [%]"]



class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self) -> None:
        self.daily_rsi = self.I(talib.RSI, self.data.Close, 14)

    def next(self) -> None:
        if crossover(self.daily_rsi, self.upper_bound):
            if self.position.is_long:  # --- Check for our position ---
                print(self.position.size)
                print(self.position.pl_pct)
                self.position.close()
                self.sell()

        elif crossover(self.lower_bound, self.daily_rsi):
            # price = self.data.Close[-1]
            if self.position.is_short or not self.position: # --- Check for our position ---
                self.position.close()
                # self.buy(tp=1.15*price, sl=0.95*price) # Take Profit / Stop Loss
                self.buy()

bt = Backtest(GOOG, RsiOscillator, cash = 10_000)

stats = bt.run()

bt.plot()

print(stats)
