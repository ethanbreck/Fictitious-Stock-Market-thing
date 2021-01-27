# Packages
import datetime
import os

# Pypi Packages
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

from mplfinance.original_flavor import candlestick_ohlc
import yfinance as yf

# code Starts below

yf.pdr_override()  # activate yahoo finance workaround

stock = input("Enter the stock symbol : ")  # Asks for stock ticker


# Functions:


def smasUsed():
    # Choose smas
    return [10, 30, 50]


def dataframeStart():
    # Sets start point of dataframe
    smas = smasUsed()
    start = datetime.datetime(2020, 1, 1) - datetime.timedelta(days=max(smas))
    return start


def getData():
    now = datetime.datetime.now()
    start = dataframeStart()
    data = pdr.get_data_yahoo(stock, start, now)
    return data


# Code

prices = getData()

app_dir = os.path.abspath(os.path.dirname(__file__))
startingData = os.path.join(app_dir, "data/data.csv")

with open(startingData, mode="a") as file:
    data = prices.to_csv(file)
    # can do JSON as well by switching filetype to .JSON after the file name, and switch prices.to_csv(file) to prices.to_json(file)


def smaCalc():
    theSma = smasUsed()
    for x in theSma:
        prices['SMA_' + str(x)] = prices.iloc[:, 4].rolling(window=x).mean()
    smaData = os.path.join(app_dir, "data/data_w_sma.csv")
    with open(smaData, mode="w") as file:
        prices.to_csv(file)
        # can do JSON as well by switching filetype to .JSON after the file name, and switch prices.to_csv(file) to prices.to_json(file)

    return None


def bBands():
    # calculate Bollinger Bands
    BBperiod = 15
    stdev = 2  # choose moving averave
    prices['SMA' + str(BBperiod)] = prices.iloc[:, 4].rolling(window=BBperiod).mean()  # calculates sma and creates a column in the dataframe
    prices['STDEV'] = prices.iloc[:, 4].rolling(window=BBperiod).std()  # calculates standard deviation and creates col
    prices['LowerBand'] = prices['SMA' + str(BBperiod)] - (stdev * prices['STDEV'])  # calculates lower bollinger band
    prices['UpperBand'] = prices['SMA' + str(BBperiod)] + (stdev * prices['STDEV'])  # calculates upper band
    prices["Date"] = mdates.date2num(prices.index)    # creates a date column stored in number format (for OHCL bars)
    bbData = os.path.join(app_dir, "data/data_w_bbands.csv")
    with open(bbData, mode="w") as file:
        prices.to_csv(file)
        # can do JSON as well by switching filetype to .JSON after the file name, and switch prices.to_csv(file) to prices.to_json(file)

    return None


if __name__ == '__main__':
    smaCalc()
    print("SMA has been added")
    bBands()
    print("Bollinger Bands have been calculated")
