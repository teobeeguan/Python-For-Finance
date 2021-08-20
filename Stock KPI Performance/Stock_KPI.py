# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 10:03:12 2021

@author: Teo Bee Guan
"""

import yfinance as yf
import numpy as np

ticker = 'aapl'
stock_data = yf.download(ticker, start='2018-08-20', end='2021-08-20')


def CAGR(data):
    df = data.copy()
    df['daily_returns'] = df['Adj Close'].pct_change()
    df['cumulative_returns'] = (1 + df['daily_returns']).cumprod()
    trading_days = 252
    n = len(df)/ trading_days
    cagr = (df['cumulative_returns'][-1])**(1/n) - 1
    return cagr

print("CAGR: " + str(CAGR(stock_data) * 100) + "%")

def volatility(data):
    df = data.copy()
    df['daily_returns'] = df['Adj Close'].pct_change()
    trading_days = 252
    vol = df['daily_returns'].std() * np.sqrt(trading_days)
    return vol

print("Annualized Volatility: " + str(volatility(stock_data) * 100) + "%")

def sharpe_ratio(data, rf):
    df = data.copy()
    sharpe = (CAGR(df) - rf)/ volatility(df)
    return sharpe 

print("Sharpe Ratio: " + str(sharpe_ratio(stock_data, 0.03)))

def sortino_ratio(data, rf):
    df = data.copy()
    df['daily_returns'] = df['Adj Close'].pct_change()
    df["negative_returns"] = np.where(df["daily_returns"]<0,df["daily_returns"],0)
    negative_volatility = df['negative_returns'].std() * np.sqrt(252)
    sortino = (CAGR(df) - rf)/ negative_volatility 
    return sortino

print("Sortino Ratio: " + str(sortino_ratio(stock_data, 0.03)))

def maximum_drawdown(data):
    df = data.copy()
    df['daily_returns'] = df['Adj Close'].pct_change()
    df['cumulative_returns'] =  (1 + df['daily_returns']).cumprod()
    df['cumulative_max'] = df['cumulative_returns'].cummax()
    df['drawdown'] = df['cumulative_max'] - df['cumulative_returns']
    df['drawdown_pct'] = df['drawdown'] / df['cumulative_max']
    max_dd = df['drawdown_pct'].max()
    return max_dd

def calmar_ratio(data, rf):
    df = data.copy()
    calmar = (CAGR(df) - rf) / maximum_drawdown(data)
    return calmar

print("Calmar Ratio: " + str(calmar_ratio(stock_data, 0.03)))
