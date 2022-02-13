# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 00:17:52 2022

@author: Teo Bee Guan
"""

import telepot 
import requests 
from datetime import datetime
from timeloop import Timeloop
from datetime import timedelta

def getStockData(ticker):
    base_url = "https://financialmodelingprep.com/api/v3/quote/"
    key = "YOUR API KEY"
    full_url = base_url + ticker + "?apikey=" + key
    r = requests.get(full_url)
    stock_data= r.json()
    return stock_data

def generateMessage(data):
    symbol = data[0]['symbol']
    price = data[0]["price"]
    changesPercent = data[0]["changesPercentage"]
    timestamp = data[0]['timestamp']
    
    current = datetime.fromtimestamp(timestamp)
    message = str(current)
    message += "\n" + symbol 
    message += "\n$" + str(price)
    
    if(changesPercent < -2):
        message += "\nWarning! Price drop more than 2%!"
        
    return message

def sendMessage(text):
    token = "YOUR TOKEN"
    receiver_id = YOUR RECEIVER ID #In Numeric Format
    bot = telepot.Bot(token)
    bot.sendMessage(receiver_id,text)
  

tl = Timeloop()

@tl.job(interval=timedelta(seconds=60))
def run_tasks():
    ticker = "AMZN"
    real_time_data = getStockData(ticker)
    textMessage = generateMessage(real_time_data)
    sendMessage(textMessage)
    
tl.start(block=True)