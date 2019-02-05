"""
Process that publishes new spot values for the underlying and also sends
out updated quotes.
"""

from multiprocessing import Process
import time
import config as cfg
import bs

class UnderlyingMarket(Process):
    """
    Process that publishes a new underlying value and regular intervals.
    We use the given process to get a new process at a given interval.
    We then calculate the options price and publish quotes to the market.
    Only after publishing the quotes we signal the underlying update to
    the other market participants.
    """
    def __init__(self, process, spotValue, spotUpdate, market, quoteWidthPerc, delay, steps):
        super(UnderlyingMarket, self).__init__()
        self.spotValue = spotValue
        self.spotUpdate = spotUpdate
        self.market = market
        self.process = process
        self.dt = cfg.DT
        self.qwidth = 1.0 + quoteWidthPerc/100.0
        self.delay = delay
        self.steps = steps


    def run(self):
        """ Run for the given number of steps"""
        for i in range(self.steps):
            spot = self.process.next(self.dt)
            # note that I ignore time decay of the option price
            theo = bs.bscall(spot, \
                    cfg.OPTION["strike"], \
                    cfg.OPTION["tau"], \
                    cfg.OPTION["rate"], \
                    cfg.OPTION["vola"])

            self.market.put([theo/self.qwidth, theo*self.qwidth, spot, self.spotUpdate.value +1])
            self.spotValue.value = spot
            self.spotUpdate.value = self.spotUpdate.value + 1
            time.sleep(self.delay)


