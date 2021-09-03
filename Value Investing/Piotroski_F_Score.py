# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 14:03:59 2021

@author: Teo Bee Guan
"""

from alpha_vantage.fundamentaldata import FundamentalData

key = 'YOUR API KEY'
fd = FundamentalData(key,output_format = 'pandas')
ticker = 'adbe'

raw_IS = fd.get_income_statement_annual(ticker)
income_statement = raw_IS[0].T[2:]
income_statement.columns = list(raw_IS[0].T.iloc[0])

raw_BS = fd.get_balance_sheet_annual(ticker)
balance_sheet = raw_BS[0].T[2:]
balance_sheet.columns = list(raw_BS[0].T.iloc[0])

raw_CS = fd.get_cash_flow_annual(ticker)
cash_flow = raw_CS[0].T[2:]
cash_flow.columns = list(raw_CS[0].T.iloc[0])

def get_net_income(income_df):
    return float(income_df.loc['netIncome'][0])

def get_roa(balance_df, income_df):
    current = float(balance_df.loc['totalAssets'][0])
    previous = float(balance_df.loc['totalAssets'][1])
    av_assets=(current+previous)/2
    return get_net_income(income_df)/av_assets

def get_ocf(cash_df):
    return float(cash_df.loc['operatingCashflow'][0])

def get_ltdebt(balance_df):
    current = float(balance_df.loc['longTermDebt'][0])
    previous = float(balance_df.loc['longTermDebt'][1])
    return previous - current

def get_current_ratio(balance_df):
    current_TCA = float(balance_df.loc['totalCurrentAssets'][0])
    previous_TCA = float(balance_df.loc['totalCurrentAssets'][1])
    current_TCL = float(balance_df.loc['totalCurrentLiabilities'][0])
    previous_TCL = float(balance_df.loc['totalCurrentLiabilities'][1])
    ratio1 = current_TCA/ current_TCL
    ratio2 = previous_TCA / previous_TCL
    return ratio1-ratio2

def get_new_shares(balance_df):
    current = float(balance_df.loc['commonStock'][0])
    previous = float(balance_df.loc['commonStock'][1])
    return current - previous 

def get_gross_margin(income_df):
    current = float(income_df.loc['grossProfit'][0])/float(income_df.loc['totalRevenue'][0])
    previous =  float(income_df.loc['grossProfit'][1])/float(income_df.loc['totalRevenue'][1])
    return current - previous

def get_asset_turnover_ratio(income_df, balance_df):
    current = float(balance_df.loc['totalAssets'][0])
    prev_1 = float(balance_df.loc['totalAssets'][1])
    prev_2 = float(balance_df.loc['totalAssets'][2])
    av_assets1=(current+prev_1)/2
    av_assets2=(prev_1+ prev_2)/2
    atr1=float(income_df.loc['totalRevenue'][0])/av_assets1
    atr2=float(income_df.loc['totalRevenue'][1])/av_assets2
    return atr1-atr2

def get_piotroski_score(income_df, balance_df, cash_df):
    score=0
    
    if get_net_income(income_df)>0:
        score +=1

    if get_roa(balance_df, income_df)>0:
        score +=1
        
    if get_ocf(cash_df)>0:
        score +=1
        
    if get_ocf(cash_df)>get_net_income(income_df):
        score +=1
        
    if get_ltdebt(balance_df)>0:
        score +=1
        
    if get_current_ratio(balance_df)>0:
        score +=1
        
    if get_new_shares(balance_df)>0:
        score +=1
        
    if get_gross_margin(income_df)>0:
        score +=1
        
    if get_asset_turnover_ratio(income_df, balance_df)>0:
        score +=1
        
    return score

print("The Piotroski F Score is: " + str(get_piotroski_score(income_statement, balance_sheet, cash_flow)))
