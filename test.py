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

# creating of global variables
app_dir = os.path.abspath(os.path.dirname(__file__))

stock = input("Enter the stock symbol : ")  # Asks for stock ticker

prices = None  # This will be a dataframe that handles storage of all the data
stochs = pd.DataFrame(data=None)  # This dataframe will handle the calculation of the various Stok functions, and subsequently be appended to prices after calculations
ohlc = []  # Create OHLC array which will store price data for the candlestick chart

# Code

yf.pdr_override()  # activate yahoo finance workaround


def getData(smas):
    now = datetime.datetime.now()
    start = datetime.datetime(2020, 1, 1) - datetime.timedelta(days=max(smas))
    data = pdr.get_data_yahoo(stock, start, now)
    return data


def smaCalc(smaNums):
    theSma = smaNums
    for x in theSma:
        prices['SMA_' + str(x)] = prices.iloc[:, 4].rolling(window=x).mean()
    smaData = os.path.join(app_dir, "data/data_w_sma.csv")
    with open(smaData, mode="w") as file:
        prices.to_csv(file)
        # can do JSON as well by switching filetype to .JSON after the file name, and switch prices.to_csv(file) to prices.to_json(file)

    return None


def smaStdev(bbperiod):
    BBperiod = bbperiod
    prices['SMA' + str(BBperiod)] = prices.iloc[:, 4].rolling(window=BBperiod).mean()  # calculates sma and creates a column in the dataframe
    prices['STDEV'] = prices.iloc[:, 4].rolling(window=BBperiod).std()  # calculates standard deviation and creates col
    return None


def lowerBand(bbperiod, stdev):
    BBperiod, stdev = bbperiod, stdev
    prices['LowerBand'] = prices['SMA' + str(BBperiod)] - (stdev * prices['STDEV'])  # calculates lower bollinger band
    return None


def upperBand(bbperiod, stdev):
    BBperiod, stdev = bbperiod, stdev
    prices['UpperBand'] = prices['SMA' + str(BBperiod)] + (stdev * prices['STDEV'])  # calculates upper band
    return None


def rolHigh(period):
    Period = period
    rolHigh = prices["High"].rolling(window=Period).max()  # Finds high of period
    return rolHigh


def rolLow(period):
    Period = period
    rolLow = prices["Low"].rolling(window=Period).min()  # finds low of period
    return rolLow


def stochPointOne(period):
    # This finds the 10.1 stochastic
    period = period
    rolLownum = rolLow(period)
    rolHihgnum = rolHigh(period)
    stok = ((prices["Adj Close"] - rolLownum) / (rolHihgnum - rolLownum)) * 100  # Finds 10.1 stoch
    return stok


def stochPointFour(k):
    # This finds 10.4 stochastic
    K = k
    data = stochs["Stok"].rolling(window=K).mean()  # Finds 10.4 stoch
    return data


def stochsPointFourFour(d):
    # This finds the 10.4.4 stochastic
    D = d
    data = stochs["K"].rolling(window=D).mean()  # Finds 10.4.4 stoch
    return data


def main():
    global prices
    global stochs
    smasused = 10, 30, 50  # This is for simple moving average's
    BBperiod = 15  # chooses Bollinger Bands
    stdev = 2  # choose moving average
    period = 100
    K = 4
    D = 4

    prices = getData(smasused)
    startingData = os.path.join(app_dir, "data/data.csv")
    with open(startingData, mode="a") as file:
        prices.to_csv(file)
    # can do JSON as well by switching filetype to .JSON after the file name, and switch prices.to_csv(file) to prices.to_json(file)
    smaCalc(smasused)
    smaStdev(BBperiod)
    lowerBand(BBperiod, stdev)
    upperBand(BBperiod, stdev)
    prices["BarsDate"] = mdates.date2num(prices.index)  # creates a date column stored in number format (for OHCL bars)
    bbanddata = os.path.join(app_dir, "data/data_w_bbands.csv")
    with open(bbanddata, mode="w") as file:
        prices.to_csv(file)
        # can do JSON as well by switching filetype to .JSON after the file name, and switch prices.to_csv(file) to prices.to_json(file)
    
    stochs["BarsDate"] = prices["BarsDate"]
    stochs["RolHigh"] = rolHigh(period)
    stochs["RolLow"] = rolLow(period)
    stochs["Stok"] = stochPointOne(period)
    stochs["K"] = stochPointFour(K)
    stochs["D"] = stochsPointFourFour(D)
    stochs["GD"] = prices["High"]  # Create GD column to store green dots (Look at using the data from the high column instead of creating a new column for this)
    print(prices)
    print(stochs)
    return None


if __name__ == '__main__':
    main()
