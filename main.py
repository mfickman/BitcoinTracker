#the purpose of this program is to use and bitcoin value tracker api
#and build a simple visualization based on the repsonse


import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc

#create API object
cg = CoinGeckoAPI()

#pull data from the past 30 days
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)
bitcoin_price_data = bitcoin_data['prices']

#use pandas to create dataframe from request data
df_bitcoin_data = pd.DataFrame(bitcoin_price_data, columns=["TimeStamp", "Price"])

#use lambda function to convert timestamp into datetime form
df_bitcoin_data['Date'] = df_bitcoin_data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))

#indentify min, max, open, and close data points per day
candlestick_data = df_bitcoin_data.groupby(df_bitcoin_data.Date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})

#build ploty image
date_now = datetime.datetime.now()
date_minus_30 = date_now - datetime.timedelta(days=30)

title_str = "Bitcoin Tracking from " + date_minus_30.strftime("%m/%d/%Y, %H:%M:%S") + " to " + date_now.strftime("%m/%d/%Y, %H:%M:%S")
fig = go.Figure(data=[go.Candlestick(x=candlestick_data['Date'],
                open=candlestick_data['Price']['first'],
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'],
                close=candlestick_data['Price']['last'])])

fig.update_layout(title=title_str,
                  title_x=0.5,
                  xaxis_rangeslider_visible=False,
                  xaxis_title="Date",
                  yaxis_title="Price (USD)")

fig.show()


