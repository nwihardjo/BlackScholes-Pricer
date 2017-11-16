import argparse
import os
import sys
import importlib
from math import exp

"""
Usage: python UnitTest.py model

models reside in the models directory, so something like models/Team13Pricer.py

This runs a few unit tests. If they fail they point you hopefully to a problem in your pricer.
Passing all unit tests is not a gurantee that your pricer is correct. We only test a few edge
cases here.

"""

def doesnotthrow(pricer):
    """ Your pricer throws an exception!!! """
    try:
        pricer(100.0, 100.0, 1.0, 0.0, 0.1)
    except:
        return False
    return True

def otmlimit(pricer):
    """ Out of the money limit test: if spot << strike your call option should have 0 price """
    otmprice = pricer(1.0, 100.0, 1.0, 0.0, 0.1)
    if abs(otmprice) > 1e-10:
        return False
    return True

def itmlimit(pricer):
    """ In the money limit test: the call price should be identical to the forward price (S-Kexp(-r*tau)). Check your discounting!"""
    spot = 100.0
    strike = 1.0
    rate = 0.05
    tau = 1.0
    itmprice = pricer(spot, strike, tau, rate, 0.05)
    ref = spot - strike*exp(-rate*tau)
    if abs(itmprice-ref) > 1e-10:
        return False
    return True

def RunTests(pricer):
    """ Run all unit tests """
    passed = True
    for test in [doesnotthrow, otmlimit, itmlimit]:
        try:
            ok = test(pricer)
        except:
            ok = False
        if not ok:
            passed = False
            print("Failed : %s"%test.__doc__)

    return passed

def loadmodel(model):
    """Try to load the model and return pricer"""
    bn = os.path.basename(model)
    if not bn.endswith(".py"):
        raise NameError("Error %s is not a python file"%model)
    modelname = "models.%s"%bn[:-3]
    importlib.import_module(modelname)
    module = sys.modules[modelname]
    return getattr(module, "pricer")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List of Models')
    parser.add_argument('model', metavar='model', help='a model to run')
    args = parser.parse_args()
    try:
        pricer = loadmodel(args.model)
    except Exception as e:
        print("Failed to Load model \"%s\""%args.model)
        print(e)
        print("\nYou probably are missing some imports")
    passed = RunTests(pricer)
    if passed:
        print("------ Unit tests passed ----------")
    else:
        print("****** SOME/ALL UNIT TESTS FAILED, PLEASE CHECK *****")




