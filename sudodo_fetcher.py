import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime
import ccxt

from crypto_data_fetcher.gmo import GmoFetcher
from crypto_data_fetcher.bybit import BybitFetcher
from crypto_data_fetcher.ftx import FtxFetcher
import joblib

GMO = "GMO"
BYBIT = "Bybit"
FTX = "FTX"

#######################
# Settings
EXCHANGE = FTX
INTERVAL = 1 # min

print(f"get ohlcv from {EXCHANGE}. Interval: {INTERVAL} min")

if EXCHANGE == GMO:
    memory = joblib.Memory('/tmp/gmo_fetcher_cache', verbose=0)
    fetcher = GmoFetcher(memory=memory)
    df = fetcher.fetch_ohlcv(
        market='BTC_JPY', # 市場のシンボルを指定
        interval_sec=INTERVAL * 60, # 足の間隔を秒単位で指定。
    )
elif EXCHANGE == BYBIT:
    fetcher = BybitFetcher(ccxt_client=ccxt.bybit())
    df = fetcher.fetch_ohlcv(
        df=None,                 
        start_time=None,
        interval_sec=INTERVAL * 60,
        market='BTCUSD',
        price_type=None)
elif EXCHANGE == FTX:
    ftx = ccxt.ftx({ "verbose": False })
    fetcher = FtxFetcher(ccxt_client=ftx)
    df = fetcher.fetch_ohlcv(
        market='BTC/USD',
        interval_sec=INTERVAL * 60,
        start_time=None
    )    

TODAY = today = datetime.now().strftime('%Y%m%d')
basename = f"{EXCHANGE}_ohlcv_{INTERVAL}minute_BTCJPY_{TODAY}"
df.to_csv(f"{basename}.csv")
plt.plot(df[["op", "hi", "lo", "cl"]])
plt.savefig(f"{basename}_ohlc.png")
plt.show()
plt.plot(df["volume"])
plt.savefig(f"{basename}_volume.png")
plt.show()