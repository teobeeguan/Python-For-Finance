# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 11:59:08 2021

@author: Teo Bee Guan
"""

import yfinance as yf

ticker = "AAPL"
stock_data = yf.download(ticker, start='2021-01-02', end="2021-01-31")

tickers = ['AAPL', 'GOOGL', 'AMZN']
stock_data = yf.download(tickers, start='2021-01-02', end="2021-01-31", group_by='ticker')


ticker = "MSFT"
fundamental_data = yf.Ticker(ticker)
print(fundamental_data.info.keys())
print(fundamental_data.info['quoteType'])
print(fundamental_data.info['currency'])
print(fundamental_data.info['sector'])
print(fundamental_data.info['grossProfits'])
print(fundamental_data.info['freeCashflow'])
print(fundamental_data.info['ebitda'])


from alpha_vantage.timeseries import TimeSeries

ticker = 'IBM'
handler = TimeSeries(key='YOUR API KEY', output_format="pandas")
stock_data = handler.get_daily_adjusted(ticker)

from alpha_vantage.fundamentaldata import FundamentalData

ticker = 'TSLA'
handler = FundamentalData(key='YOUR API KEY',output_format = 'pandas')
income_statement = handler.get_income_statement_annual(ticker)
balance_sheet = handler.get_balance_sheet_annual(ticker)
cash_flow = handler.get_cash_flow_annual(ticker)

from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt

ticker = 'TSLA'
handler = TechIndicators(key='YOUR API KEY', output_format='pandas')
technical_data, meta_data = handler.get_bbands(ticker, interval='60min', time_period=60)
technical_data.plot()
plt.title('BBbands indicator for  TSLA stock (60 min)')
plt.show()

import pandas_datareader as pdr
fed_data = pdr.get_data_fred('GS10')
fed_data.plot()
plt.title('10-year Constant Maturity Yields on US Government Bonds')
plt.show()

from pandas_datareader import wb
wb_data = wb.download(indicator='NY.GDP.PCAP.KD', country=['US', 'CA'], start=2016, end=2020)

