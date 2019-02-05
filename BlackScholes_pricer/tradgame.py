from TradingGame import TradingGame
from EventPlot import EventPlot
import functools

def partial(model, steps):
    f = functools.partial(model, steps=steps)
    f.__name__ = "%s:%d"%(model.__name__, steps)
    return f

