# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 23:39:35 2021

@author: Teo Bee Guan
"""

import requests
from bs4 import BeautifulSoup 
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

analyser = SentimentIntensityAnalyzer()
print(df['text'][4])
print(analyser.polarity_scores(df['text'][4]))

def calc_sentiment_score(text):
    return analyser.polarity_scores(text)["compound"]

analyser = SentimentIntensityAnalyzer()
df['sentiment_score'] = df['text'].apply(calc_sentiment_score)

df['sentiment_score'].plot(kind='bar', figsize=(10,5))
