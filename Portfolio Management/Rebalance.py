# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 17:31:11 2021

@author: Teo Bee Guan
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

tickers = ["AAPL", "ABMD", "ACN", "ADBE", "AEE", "AMZN", "COG", "CPB", "CVX",
           "DLR", "DLTR", "DPZ", "EA", "EBAY", "FB", "FDX", "FOX", "GE","GOOGL",  
           "HPE", "HD", "HON", "IEX", "INTC", "JNJ", "JPM", "KMB", "LRCX", 
           "MAR", "MA", "MSFT", "MSI",  "NFLX", "NKE", "NLSN", "ORCL", "PYPL", 
           "PFE",  "QCOM", "REG", "SBUX", "TSLA", "TWTR", "UAL", "VZ",  "WFC", 
           "WDC", "XEL", "YUM", "ZION"]

stock_data = yf.download(tickers,start='2019-04-1', end='2021-08-1',interval='1mo')
stock_data = stock_data.dropna()     

sp500 = yf.download("^GSPC",start='2019-4-1', end='2021-08-1',interval='1mo')

stock_returns = pd.DataFrame()

for ticker in tickers:
    stock_returns[ticker] = stock_data['Adj Close'][ticker].pct_change()

stock_returns = stock_returns.dropna()

sp500["monthly_returns"] = sp500["Adj Close"].pct_change().fillna(0)

def portfolio(data, numStocks, numRev):
    df = data.copy()
    selected_stocks = []
    avg_monthly_ret = [0]
    for i in range(len(df)):
        if len(selected_stocks ) > 0:
            avg_monthly_ret.append(df[selected_stocks].iloc[i,:].mean())
            bad_stocks = df[selected_stocks].iloc[i,:].sort_values(ascending=True)[:numRev].index.values.tolist()
            selected_stocks  = [t for t in selected_stocks if t not in bad_stocks]
        fill = numStocks - len(selected_stocks)
        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        selected_stocks  = selected_stocks  + new_picks
        print(selected_stocks)
    returns_df = pd.DataFrame(np.array(avg_monthly_ret),columns=["monthly_returns"])
    return returns_df 


def CAGR(data):
    df = data.copy()
    df['cumulative_returns'] = (1 + df['monthly_returns']).cumprod()
    trading_months = 12
    n = len(df)/ trading_months
    cagr = (df['cumulative_returns'][len(df)-1])**(1/n) - 1
    return cagr

def volatility(data):
    df = data.copy()
    trading_months = 12
    vol = df['monthly_returns'].std() * np.sqrt(trading_months)
    return vol

def sharpe_ratio(data, rf):
    df = data.copy()
    sharpe = (CAGR(df) - rf)/ volatility(df)
    return sharpe 

def maximum_drawdown(data):
    df = data.copy()
    df['cumulative_returns'] =  (1 + df['monthly_returns']).cumprod()
    df['cumulative_max'] = df['cumulative_returns'].cummax()
    df['drawdown'] = df['cumulative_max'] - df['cumulative_returns']
    df['drawdown_pct'] = df['drawdown'] / df['cumulative_max']
    max_dd = df['drawdown_pct'].max()
    return max_dd
    

rebalanced_portfolio = portfolio(stock_returns, 5, 2)
print("Rebalanced Portfolio Performance")
print("CAGR: " + str(CAGR(rebalanced_portfolio)))
print("Sharpe Ratio: " + str(sharpe_ratio(rebalanced_portfolio, 0.03)))
print("Maximum Drawdown: " + str(maximum_drawdown(rebalanced_portfolio) ))

print("\n")

print("S&P500 Index Performance")
print("CAGR: " + str(CAGR(sp500)))
print("Sharpe Ratio: " + str(sharpe_ratio(sp500, 0.03)))
print("Maximum Drawdown: " + str(maximum_drawdown(sp500) ))

fig, ax = plt.subplots()
plt.plot((1+portfolio(stock_returns, 5, 2)).cumprod())
plt.plot((1+sp500["monthly_returns"].reset_index(drop=True)).cumprod())
plt.title("S&P500 Index Return vs Rebalancing Strategy Return")
plt.ylabel("cumulative return")
plt.xlabel("months")
ax.legend(["Strategy Return","Index Return"])

