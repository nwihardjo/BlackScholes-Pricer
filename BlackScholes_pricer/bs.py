"""
Analytical BS implementation that should be used as a reference to test pricer implementations.
"""

from math import log, sqrt, exp
from scipy.stats import norm

def bscall(spot, strike, tau, rate, vola):
    """ Call price calculated using analytical BS formula."""
    d1 = (log(spot/strike) + (rate+0.5*vola*vola)*tau)/(vola*sqrt(tau))
    d2 = d1 - vola*sqrt(tau)
    return spot*norm.cdf(d1)-strike*exp(-rate*tau)*norm.cdf(d2)

def bsput(spot, strike, tau, rate, vola):
    """ Put price calculated using analytical BS formula."""
    d1 = (log(spot/strike) + (rate+0.5*vola*vola)*tau)/(vola*sqrt(tau))
    d2 = d1 - vola*sqrt(tau)
    return strike*exp(-rate*tau)*norm.cdf(-d2)-spot*norm.cdf(-d1)


