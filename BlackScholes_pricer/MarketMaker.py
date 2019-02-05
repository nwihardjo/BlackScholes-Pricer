"""
Process that represents a market maker: it listens to spot updates
and then publishes a theoretical value for the option price.
"""
from multiprocessing import Process
import config as cfg
import time

class MarketMaker(Process):
    """
    Listen to spot updates, calculate a theoretical price with the given model
    and publish it.
    """
    def __init__(self, pricerId, spotValue, spotUpdate, market, model):
        super(MarketMaker, self).__init__()
        self.pricerId = pricerId
        self.spotValue = spotValue
        self.spotUpdate = spotUpdate
        self.mm = market
        self.model = model
        self.spotCounter = 0

    def run(self):
        while 1:
            while self.spotUpdate.value == self.spotCounter:
                pass
            self.spotCounter = self.spotUpdate.value
            spot = self.spotValue.value
            theo = self.model(spot, \
                    cfg.OPTION["strike"], \
                    cfg.OPTION["tau"], \
                    cfg.OPTION["rate"], \
                    cfg.OPTION["vola"])
            self.mm.put((self.pricerId, theo, spot, self.spotCounter))

