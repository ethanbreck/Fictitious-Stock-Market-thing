# Here are some of my notes while I work on OHLC_1.PY

Are Numpy and Pandas neeeded?

Why is ```prices["Date"] = mdates.date2num(prices.index)  # creates a date column stored in number format (for OHCL bars)``` there? Can the normal date not be used for datetime stuff? Can the datetime string not be converted in real time for each datapoint? Why is this datapoint used for mathplotlib? 

For the prices["GD"] or now created stoch["GD"] column, why is that being used as a thing, if its just using the data from prices["high"], without any changes?