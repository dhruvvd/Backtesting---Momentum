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

analysis['returns'] = df['close'].pct_change()
analysis['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()
analysis['SMA_50'] = df['close'].rolling(50).mean()

analysis.dropna(inplace=True)

# -- BUY / SELL LOGIC --

def buy_order(df):
    pass