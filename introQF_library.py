# ---------------------------------
# Importing all necessary libraries
# ---------------------------------
# libraries that come with ANACONDA
try:
    import numpy as np
    from scipy.stats import t, norm, lognorm
    from scipy.special import comb
    from pandas import read_csv
except ImportError as e:
    print(e)
    raise Exception("ANACONDA may not have been installed properly?")

# ---------------------------------
# specific libraries
try:
    # needed to extract quotes from Yahoo Finance website
    from requests import get as getURL
except ImportError:
    raise Exception("REQUESTS may not have been installed properly, please try entering \"pip install requests\" in your terminal.")

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import seaborn as sns
except ImportError:
    raise Exception("MATPLOTLIB or SEABORN may not have been installed properly, please try entering \"pip install matplotlib seaborn\" in your terminals.")
    
# -----
# other
from os.path import isfile
from time import time

# -------------------------------------------
# Simple functions defined to retrieve quotes
# from Yahoo finance.
def nFile(sym,yStart,yEnd):
    """
        Build a file-name to store data about symbol SYM over specific date range
    """
    assert sym==str(sym), "Symbol name should be a string"
    return "pdata_"+sym.upper()+"_"+str(yStart)+"_"+str(yEnd)+".csv"
#
def getSymbol(sym,yStart,yEnd):
    """
        Retrieve financial symbol (SYM) over period of time (YSTART-YEND).
        Yahoo Finance stores values as
        Date[0], Open[1], High[2], Low[3], Close[4], Volume[5], Adj Close[6].
    """
    # Ensure input is sensible
    assert yStart==int(yStart) and yEnd==int(yEnd), "yStart, yEnd should be integers"
    assert 1990 < yStart < yEnd < 2016, "yStart, yEnd should be an interval of 1990-2016"
    #
    try:
        # Links for Yahoo Finance
        base  = "http://ichart.finance.yahoo.com/table.csv?d=6&e=1&f="
        link  = base + str(yEnd) + "&g=d&a=7&b=19&c="
        link += str(yStart) + "&ignore=.csv&s=" + sym.upper()
        # read content of link (raw text)
        t = getURL(link)
        # file name to save content
        nfile = nFile(sym,yStart,yEnd)
        # write to file
        with open(nfile,'w') as f: f.write(t.text)
    except:
        raise Exception("..invalid link.. did you enter a valid symbol?")
#
def getPrices(sym,yStart,yEnd,wDates=True):
    """
        Retrieve closing price of symbol (SYM) over period of time (YSTART-YEND).
    """
    nfile = nFile(sym,yStart,yEnd)
    if not(isfile(nfile)):
        getSymbol(sym,yStart,yEnd)
    #
    ret = 0.
    if not(wDates):
        ret = np.array(read_csv(nfile))[:,4].astype(np.float32)[::-1]
    else:
        conv  = mdates.strpdate2num('%Y-%m-%d')
        dates = np.array(read_csv(nfile))[:,0][::-1] 
        ret   = ([conv(d) for d in dates],
                   np.array(read_csv(nfile))[:,4].astype(np.float32)[::-1])
    return ret
