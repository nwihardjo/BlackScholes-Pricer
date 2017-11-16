"""
This Module defines a log normally distributed underlying process.
"""

from math import log, sqrt, exp
import numpy as np


class LogNormalUnderlying:
    """
    Log-normal underlying process: determined by the initial spot, risk-free rate and volatility.
    """

    def __init__(self, spot, rate, vola):
        """Args: initial spot, risk free rate and volatility"""
        self.rate = rate
        self.vola = vola
        self.x = log(spot)

    def next(self, dt):
        """Return current underlying value after a time step dt (in years)"""
        self.x = self.x + \
                (self.rate-0.5*self.vola*self.vola)*dt + \
                sqrt(dt)*self.vola*np.random.normal()
        return exp(self.x)


