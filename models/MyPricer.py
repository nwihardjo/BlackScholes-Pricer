
from tradgame import *

"""

This is a template which you can use to create your own pricer. Just make sure to rename the function
'MyPricer' to reflect your team name or give it some other name.

"""


def MyPricer(spot, strike, tau, rate, vola, steps):
    """
    This is where all the action is. You should return the price of the call option
    """
    return 0

# The function you expose here is used in the test. Use 'partial' to decide on the number of steps
pricer = partial(MyPricer, 100)

