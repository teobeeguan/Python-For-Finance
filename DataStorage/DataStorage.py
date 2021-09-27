# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 11:18:50 2021

@author: Teo Bee Guan
"""

import psycopg2
import yfinance as yf
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

ticker = 'AAPL'
stock_data = yf.download(ticker, start='2021-8-1', end="2021-9-1")
stock_data.index = np.datetime_as_string(stock_data.index, unit='D')
stock_data['Ticker'] = ticker
stock_data = stock_data.rename(columns={"Adj Close": "Adj_Close"})
records = stock_data.to_records(index=True)

conn = psycopg2.connect(
   database="postgres", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True
cursor = conn.cursor()
sql = '''CREATE DATABASE stocks''';
cursor.execute(sql)
print("Database created successfully!")
conn.close()

conn = psycopg2.connect(
    database="stocks", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True
cur = conn.cursor()
cur.execute('''CREATE TABLE prices
               (
                Date DATE NOT NULL,
                Open FLOAT NOT NULL,
                High FLOAT NOT NULL,
                Low FLOAT NOT NULL,
                Close FLOAT NOT NULL,
                Adj_Close FLOAT NOT NULL,
                Volume BIGINT NOT NULL,
                Ticker VARCHAR(255) NOT NULL
                );''')
               
print("Table created successfully")
conn.close()

conn = psycopg2.connect(
    database="stocks", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True
cur = conn.cursor()
query = """INSERT INTO prices (Date, Open, High, Low, Close, Adj_Close, Volume, Ticker)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
cur = conn.cursor()
cur.executemany(query, records)
conn.close()
print("Data Insert Successfully")

conn = psycopg2.connect(
    database="stocks", user='postgres', password='password', host='127.0.0.1', port= '5432'
)
conn.autocommit = True
cur = conn.cursor()
cur.execute("SELECT * from prices LIMIT 5")
rows = cur.fetchall()
for row in rows:
    print(row)

print("Query done successfully");
conn.close()



               

