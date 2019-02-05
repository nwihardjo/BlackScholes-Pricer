"""
Process that listens so quote and theoretical updates.
"""

from multiprocessing import Process
import time

class OptionMarket(Process):
    """
    Record all quote and theoretical updates.
    """

    def __init__(self, spotSource, marketMaker, events):
        super(OptionMarket, self).__init__()
        self.ss = spotSource
        self.mm = marketMaker
        self.events = events
        self.quote = None
        self.theo = None
        self.quotes = []
        self.theos = []
        self.count = 0
        self.org = time.time()

    def run(self):
        while 1:
            if not self.ss.empty():
                self.events.append((time.time()-self.org, 'Q', self.ss.get()))
            if not self.mm.empty():
                self.events.append((time.time()-self.org, 'T', self.mm.get()))

