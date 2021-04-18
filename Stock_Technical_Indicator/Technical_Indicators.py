# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 11:22:50 2021

@author: Teo Bee Guan
"""

import talib
import yfinance as yf
import matplotlib.pyplot as plt


stock_data = yf.download("AAPL", start="2020-04-01", end="2021-04-15")
plt.plot(stock_data['Close'], color='blue')
plt.title("Daily Close Price (AAPL)")
plt.show()

stock_data['SMA_20'] = talib.SMA(stock_data['Close'], timeperiod=20)
stock_data['SMA_50'] = talib.SMA(stock_data['Close'], timeperiod=50)

plt.plot(stock_data['Close'], color='blue', label='Daily Close Price')
plt.plot(stock_data['SMA_20'], color='green', label='SMA 20')
plt.plot(stock_data['SMA_50'], color='red', label='SMA 50')
plt.legend()
plt.title('Simple Moving Averages')
plt.show()


stock_data['EMA_20'] = talib.EMA(stock_data['Close'], timeperiod=20)
stock_data['EMA_50'] = talib.EMA(stock_data['Close'], timeperiod=50)

plt.plot(stock_data['Close'], color='blue', label='Daily Close Price')
plt.plot(stock_data['EMA_20'], color='green', label='EMA 20')
plt.plot(stock_data['EMA_50'], color='red', label='EMA 50')
plt.legend()
plt.title('Exponential Moving Averages')
plt.show()

plt.plot(stock_data['Close'], color='blue', label='Daily Close Price')
plt.plot(stock_data['SMA_50'], color='green', label='SMA 50')
plt.plot(stock_data['EMA_50'], color='red', label='EMA 50')
plt.legend()
plt.title('SMA 50 vs EMA 50')
plt.show()


stock_data['ADX'] = talib.ADX(stock_data['High'], stock_data['Low'], stock_data['Close'], timeperiod=14)
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_ylabel('Price')
ax1.plot(stock_data['Close'])
ax2.set_ylabel('ADX')
ax2.plot(stock_data['ADX'], color='green')
ax1.set_title('Daily Close Price and ADX')
ax2.axhline(y = 50, color = 'r', linestyle = '-')
ax2.axhline(y = 25, color = 'r', linestyle = '-')
plt.show()

macd, macdsignal, macdhist = talib.MACD(stock_data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_ylabel('Price')
ax1.plot(stock_data['Close'])
ax2.set_ylabel('MACD')
ax2.plot(macdsignal, color='green', label='Signal Line')
ax2.plot(macd, color='red', label='MACD')
ax2.bar(macdhist.index, macdhist, color='purple')
ax1.set_title('Daily Close Price and MACD')
plt.legend()
plt.show()

stock_data['RSI'] = talib.RSI(stock_data['Close'], timeperiod=14)
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_ylabel('Price')
ax1.plot(stock_data['Close'])
ax2.set_ylabel('RSI')
ax2.plot(stock_data['RSI'], color='green')
ax2.axhline(y = 70, color = 'r', linestyle = '-')
ax2.axhline(y = 30, color = 'r', linestyle = '-')
ax1.set_title('Daily Close Price and RSI')
plt.show()

upper, mid, lower = talib.BBANDS(stock_data['Close'], nbdevup=2, nbdevdn=2, timeperiod=20)
plt.plot(upper, label="Upper band")
plt.plot(mid, label='Middle band')
plt.plot(lower, label='Lower band')
plt.title('Bollinger Bands')
plt.legend()
plt.show()


