import backtrader as bt
import backtrader.feeds as btfeeds

import datetime
import pandas as pd

import schwabdev

import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# -- DATA INITIALIZATION
app_key = os.getenv("APP_KEY")
app_secret = os.getenv("APP_SECRET")

client = client = schwabdev.Client(app_key, app_secret)

data = client.price_history(symbol='NVDA', periodType='year', period=10, frequencyType='daily').json()['candles']
df = pd.DataFrame(data)

df['datetime'] = pd.to_datetime(df['datetime'], unit='ms').dt.strftime('%m-%d-%Y')
df.set_index(inplace=True, keys="datetime")

# -- INDICATOR GENERATION -- 
analysis = pd.DataFrame()
analysis.index = df.index

analysis['returns'] = df['close'].pct_change()
analysis['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()
analysis['SMA_50'] = df['close'].rolling(50).mean()
analysis['crossover'] = analysis['EMA_20'] - analysis['SMA_50']

analysis.dropna(inplace=True)

# -- SIGNAL GENERATOR LOGIC --

def signal_gen(df):
    df['signal'] = 0
    df['c_shifted'] = df['crossover'].shift(1)
    df.dropna(inplace=True)

    df[df['c_shifted'] < 0 & df['crossover'] > 0, 'signal'] = 1
    df[df['c_shifted'] > 0 & df['crossover'] < 0, 'signal'] = 2

    df['b_date'] = df[df['signal'] == 1, df.index]
    df['s_date'] = df[df['signal'] == 2, df.index]


# -- CALCULATING PROFITS / LOSSES

def calc_pl(signals, price_data, size, commission):
    buys = pd.Series()
    sells = pd.Series()
    combined = signals.join(price_data)

    combined['o_shifted'] = combined['open'].shift(-1)

    buys = combined[combined['signal'] == 1, 'o_shifted']
    sells = combined[combined['signal'] == 2, 'close']

    commission_b = commission * buys
    commission_s = commission * sells

    total_commission = commission_b + commission_s

    perc_pnl = ((sells - buys) / buys) * 100
    pnl = sells - buys
    return pnl, perc_pnl, total_commission