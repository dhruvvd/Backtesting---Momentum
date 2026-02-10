import pandas as pd
import numpy as np


class MetricCalculator():
    def cagr(starting_eq, ending_eq, length_of_strat):
        years = length_of_strat / 365
        return np.pow(ending_eq / starting_eq, 1 / years) - 1

    def sharpRatio(mean_ret, rf_rate, ret_std):
        return (mean_ret - rf_rate) / ret_std

    def sortinoRatio(mean_ret, rf_rate, retdo_std):
        return (mean_ret - rf_rate) / retdo_std

    def hitRate():
        pass

    def turnover():
        pass

    def maxDrawdown(df):
        pass