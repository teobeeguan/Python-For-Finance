# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 14:06:17 2021

@author: Teo Bee Guan
"""

import requests
from bs4 import BeautifulSoup 
import pandas as pd

ticker = "AAPL"
url = "https://financialmodelingprep.com/financial-summary/" + ticker
request = requests.get(url)
print(request.text)

parser = BeautifulSoup(request.text, "html.parser")
news_html = parser.find_all('a', {'class': 'article-item'})
print(news_html[0])

sentiments = []
for i in range(0, len(news_html)):
    sentiments.append(
            {
                'ticker': ticker,
                'date': news_html[i].find('h5', {'class': 'article-date'}).text,
                'title': news_html[i].find('h4', {'class': 'article-title'}).text,
                'text': news_html[i].find('p', {'class': 'article-text'}).text
            }
        )

df = pd.DataFrame(sentiments)
df = df.set_index('date')