import pandas as pd
import numpy as np


class MetricCalculator():
    def __init__(self, equity_curve, rf_annual):
        self.data = equity_curve
        self.returns = equity_curve.pct_change.dropna()
        self.rf_annual = rf_annual

        self.rf_daily = (1 + self.rf_annual)**(1/252) - 1

    def mean_return(self, annualize):
        mean = self.returns.mean()
        
        if annualize:
            return mean * 252
        
        return mean
    
    def std_return(self, annualize):
        daily_std = self.returns.std()

        if annualize:
            return daily_std * np.sqrt(252)
        
        return daily_std

    def downside_deviation(self, annualize):
        negative_returns = self.returns.copy()
        negative_returns[negative_returns > 0] = 0
        
        std = negative_returns.std()
        
        if annualize:
            return std * np.sqrt(252)
        return std
    
    def cagr(self, starting_eq, ending_eq, length_of_strat):
        years = length_of_strat / 252
        return np.pow(ending_eq / starting_eq, 1 / years) - 1

    def sharpRatio(self):
        excess_rets = self.mean_returns(annualize=False) - self.rf_daily

        return excess_rets / self.std_return(annualize=False)

    def sortinoRatio(self):
        excess_rets = self.mean_returns(annualize=False) - self.rf_daily

        return excess_rets / self.downside_deviation(annualize=False)

    def hitRate(self, trades_won, total_trades):
        return (trades_won / total_trades) * 100 if total_trades > 0 else 0

    def turnover(self, buy_total, sell_total):
        return min(buy_total, sell_total) / self.data.mean()

    def maxDrawdown(self):
        rolling_max = self.data.cummax()
        drawdown = abs( (self.data - rolling_max) / rolling_max )
        max_dd = drawdown.max()
        avg_dd = drawdown[drawdown > 0].mean()

        print(f"Max Drawdown: {max_dd:.2%}")
        print(f"Average Drawdown: {avg_dd:.2%}")