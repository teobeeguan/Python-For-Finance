# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 11:42:26 2021

@author: Teo Bee Guan
"""

import yfinance as yf
import mplfinance as mpf 
import numpy as np

ticker = "AAPL"
data = yf.download(ticker, start="2021-01-01", end="2021-09-1")
mpf.plot(data)

mpf.plot(data, type='candle')

data = yf.download(ticker, start="2021-01-01", end="2021-09-1")
mpf.plot(data, type='renko')
mpf.plot(data, type='pnf')

mpf.plot(data, type='candle', mav=8)
mpf.plot(data, type='candle', mav=(8, 20, 50))
mpf.plot(data, type='candle', mav=(8, 20, 50), volume=True)


data['MA20'] = data['Adj Close'].rolling(20).mean()
data['MA50'] = data['Adj Close'].rolling(50).mean()
data = data.dropna()

buy_signals = []
sell_signals = []

for i in range(len(data)):
    if (data['MA20'].iloc[i] > data['MA50'].iloc[i]) and (data['MA20'].iloc[i-1] < data['MA50'].iloc[i-1]):
        buy_signals.append(data.iloc[i]['Adj Close'] * 0.98)
    else:
        buy_signals.append(np.nan)
    
    if (data['MA20'].iloc[i] < data['MA50'].iloc[i]) and (data['MA20'].iloc[i-1] > data['MA50'].iloc[i-1]):
        sell_signals.append(data.iloc[i]['Adj Close'] * 1.02)
    else:
        sell_signals.append(np.nan)
        

buy_markers = mpf.make_addplot(buy_signals, type='scatter', markersize=120, marker='^')
sell_markers = mpf.make_addplot(sell_signals, type='scatter', markersize=120, marker='v')
apds = [buy_markers, sell_markers]
mpf.plot(data, type="candle", addplot=apds)

