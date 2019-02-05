#!/usr/bin/env python

"""
Driver for the trading game.
"""

import time
import numpy as np
from multiprocessing import Queue, Value, Manager
import pandas as pd

from PnlCalculator import calculate_pnl
from UnderlyingMarket import UnderlyingMarket
from MarketMaker import MarketMaker
from OptionMarket import OptionMarket
from LogNormalUnderlying import LogNormalUnderlying
import config as cfg


class TradingGame:
    """
    Run a Trading Game and record the events. Participants are also ranked.
    """

    def __init__(self, parameters):
        self.seed = parameters["seed"]
        self.quoteWidth = parameters["quotewidth"]
        self.delay = parameters["delay"]
        self.steps = parameters["steps"]
        self.events = []
        self.iids = {}

    def run(self, participants):
        """Run the game."""
        np.random.seed(self.seed)
        spotProcess = LogNormalUnderlying(cfg.OPTION["strike"], cfg.OPTION["rate"], \
                                          cfg.OPTION["vola"])
        spotValue = Value('f', -1.0)
        spotUpdate = Value('i', 0)
        quotePublish = Queue()
        marketPublish = Queue()
        ss = UnderlyingMarket(spotProcess, spotValue, spotUpdate, quotePublish, self.quoteWidth, \
                              self.delay, self.steps)
        manager = Manager()
        events = manager.list()
        mm = OptionMarket(quotePublish, marketPublish, events)
        mm.start()
        pricers = []
        iid = 1
        for func in participants:
            pricers.append(MarketMaker(iid, spotValue, spotUpdate, marketPublish, func))
            self.iids[iid] = func.__name__
            iid = iid + 1

        for pricer in pricers:
            pricer.start()

        time.sleep(0.1)
        ss.start()
        ss.join()
        for pricer in pricers:
            pricer.terminate()
        quotePublish.close()
        marketPublish.close()
        mm.terminate()
        ss.terminate()

        # copy events to normal list
        for a in events:
            self.events.append(a)
        print("Fini. Recorded %d events." % len(self.events))

    def getEvents(self):
        """Return the raw list of events"""
        # convert to DataFrame
        tmp = {"IID": [], "Type": [], "Bid": [], "Ask": [], "Spot": [], "Time": [], "Theo": [], "Counter": []}
        for event in self.events:
            tmp["Time"].append(event[0])
            if event[1] == 'Q':
                tmp["Type"].append('Quote')
                tmp["Bid"].append(event[2][0])
                tmp["Ask"].append(event[2][1])
                tmp["Spot"].append(event[2][2])
                tmp["Counter"].append(event[2][3])
                tmp["Theo"].append(np.nan)
                tmp["IID"].append(-1)
            else:
                tmp["Type"].append('Theo')
                tmp["Bid"].append(np.nan)
                tmp["Ask"].append(np.nan)
                tmp["Spot"].append(event[2][2])
                tmp["Counter"].append(event[2][3])
                tmp["Theo"].append(event[2][1])
                tmp["IID"].append(event[2][0])

        return pd.DataFrame(tmp)

    def ranking(self):
        """Return a DataFrame with the fails and average midmarket'ness."""
        fails = {}
        theos = {}
        delays = {}
        pnls = {}
        for iid in self.iids:
            fails[iid] = (0, 0.0, 0.0)
            theos[iid] = 0
            delays[iid] = []
            pnls[iid] = 0

        quote = None
        lastQuoteUpdate = None
        for event in self.events:
            if event[1] == 'T' and not quote:
                pass
            if event[1] == 'Q':
                quote = event[2]
                lastQuoteUpdate = event[0]
                for iid in self.iids:
                    theo = theos[iid]
                    if (theo < quote[0]) or (theo > quote[1]):
                        fails[iid] = (fails[iid][0] + 1, fails[iid][1])
                    else:
                        if (theo > 0):
                            fails[iid] = (fails[iid][0], fails[iid][1] + \
                                          abs(theo - 0.5 * (quote[0] + quote[1])))
                    pnls[iid] = pnls[iid] + calculate_pnl(quote[0], quote[1], theo)
            if event[1] == 'T':
                iid = event[2][0]
                theos[iid] = event[2][1]
                delays[iid].append(event[0] - lastQuoteUpdate)
        # convert dictionary to DataFrame
        tmp = {"Name": [], "Crossing": [], "MidMarketness": [], "Delays": [], "PnL": []}
        for iid in self.iids:
            tmp["Name"].append(self.iids[iid])
            tmp["Crossing"].append(fails[iid][0])
            tmp["MidMarketness"].append(np.mean(fails[iid][1]))
            tmp["Delays"].append(np.mean(delays[iid]))
            tmp['PnL'].append(pnls[iid])

        return pd.DataFrame(tmp, index=self.iids.keys()).sort_values(by="PnL", ascending=False)
