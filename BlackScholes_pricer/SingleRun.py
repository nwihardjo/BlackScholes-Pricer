from tradgame import *
import os
import pandas as pd
import argparse

"""
Usage: python SingleRun.py [-h] [--delay delay] models [models ...]

models reside in the models directory, so something like models/Team13Pricer.py

If your plot looks funny, try increasing the delay in the market: --delay=0.1

"""

gameParameters = {"seed" : 932748239, "quotewidth" : 0.3, "delay" : 0.001, "steps" : 200}
import sys
from models import *

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='List of Models')
    parser.add_argument('models', metavar='models', nargs='+',
                               help='a list of models to run')
    parser.add_argument('--delay', metavar='delay', type=float, help='delay in seconds')
    parser.add_argument('--seed', metavar='seed', type=int, help='seed for rng')

    args = parser.parse_args()

    if args.delay:
        gameParameters['delay'] = args.delay
    if args.seed:
        gameParameters['seed'] = args.seed

    # compatibility python2/3
    try:
        input = raw_input
    except NameError:
        pass


    models = []
    for model in args.models:
        bn =os.path.basename(model)
        if not bn.endswith(".py"):
            print("Error %s is not a python file"%bb)
            sys.exit(-1)
        module = sys.modules["models.%s"%bn[:-3]]
        models.append(getattr(module, "pricer"))

    game = TradingGame(gameParameters)
    game.run(models)
    fout = open("events", "w")
    fout.write("%s"%game.getEvents())
    fout.close()
    pp = EventPlot(game)
    pp.plot()
    print(game.ranking())
    input("Any key to close plot")
    pp.close()
    sys.exit(0)
