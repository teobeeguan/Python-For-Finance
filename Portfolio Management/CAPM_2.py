# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 18:01:00 2021

@author: Teo Bee Guan
"""

import pandas as pd
import yfinance as yf
import statsmodels.api as sm
import getFamaFrenchFactors as gff

ticker = "AMZN"
stock_data = yf.download(ticker, start="2016-06-30", end="2021-07-31")

stock_prices = stock_data['Adj Close']
stock_prices = stock_prices.resample("1M").last()
returns = stock_prices.pct_change()
returns = returns.dropna()
returns.name = "Asset"

ff3_monthly = pd.DataFrame(gff.famaFrench3Factor(frequency='m'))
ff3_monthly.rename(columns={"date_ff_factors": 'Date'}, inplace=True)
ff3_monthly.set_index('Date', inplace=True)
ff_data = ff3_monthly.merge(returns, on='Date')
rf = ff_data['RF'].mean()
market_premium = ff_data['Mkt-RF'].mean()

X = ff_data['Mkt-RF']
ff_data['Asset-RF'] = ff_data['Asset'] - ff_data['RF']
y = ff_data['Asset-RF']
c = sm.add_constant(X)
capm_model = sm.OLS(y, c)
result = capm_model.fit()
print(result.summary())
intercept, beta = result.params

expected_return = rf + beta*market_premium
print("Expected monthly returns: " + str(expected_return))
yearly_return = expected_return * 12
print("Expected yearly returns: " + str(yearly_return))
