"""
Tool to plot the recorded events.
"""

import operator
import matplotlib.pyplot as plt
import numpy as np

from PnlCalculator import calculate_pnl


class EventPlot:
    """
    Taking all the events this class displays the quotes and the theoreticals
    one update after each other.
    """

    def __init__(self, game):
        self.game = game
        self.events = game.events
        self.ranges = self.determineRanges()
        self.colors = self.determineColors()

    def close(self):
        plt.close()

    def determineColors(self):
        iids = {}
        for event in self.events:
            if event[1] == 'T':
                iids[event[2][0]] = 1
        self.iids = list(iids.keys())
        cols = {}
        tmp = plt.get_cmap('jet')(np.linspace(0, 1.0, len(self.iids)))
        i = 0
        for iid in self.iids:
            cols[iid] = tmp[i]
            i = i + 1
        return cols

    def determineRanges(self):
        xr = None
        yr = None
        for event in self.events:
            if not xr:
                xr = [event[0], event[0]]
                if event[1] == 'Q':
                    yr = [event[2][0], event[2][1]]
                else:
                    yr = [event[2][1], event[2][1]]
            else:
                xr[1] = event[0]
                if event[1] == 'Q':
                    yr[0] = min(yr[0], event[2][0])
                    yr[1] = max(yr[1], event[2][1])
                else:
                    yr[0] = min(yr[0], event[2][1])
                    yr[1] = max(yr[1], event[2][1])
        return (xr, yr)

    def extractBidAsk(self):
        x = list()
        bid = list()
        ask = list()
        for event in self.events:
            if event[1] == 'Q':
                x.append(event[0])
                bid.append(event[2][0])
                ask.append(event[2][1])
        return x, bid, ask

    def scoreString(self, fails):
        """Construct Score String"""
        tmp = sorted(fails.items(), key=operator.itemgetter(1), reverse=True)
        score = ""
        for x in tmp:
            if not score == "":
                score = score + "\n"
            score = score + "%s : GBP %d" % (self.game.iids[x[0]], x[1])
        return score

    def plot(self, delay=0.001):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.axis([self.ranges[0][0], self.ranges[0][1], self.ranges[1][0], self.ranges[1][1]])

        legs = []
        x = list()
        xfull, bid, ask = self.extractBidAsk()
        plt.grid()
        plt.plot(xfull, bid, color='#C0C0C0', drawstyle='steps-post')
        plt.plot(xfull, ask, color='#C0C0C0', drawstyle='steps-post')

        lines = {}
        legs = []
        names = []
        fails = {}
        pnls = {}
        theosNow = {}
        for iid in self.iids:
            lines[iid], = ax.plot(list(), list(), color=self.colors[iid], marker='x', \
                                  drawstyle='steps-post')
            legs.append(lines[iid])
            names.append(self.game.iids[iid])
            fails[iid] = 0
            pnls[iid] = 0
            theosNow[iid] = 0
        plt.legend(legs, names)
        plt.suptitle(self.scoreString(pnls), fontsize=14, color='red')

        theos = {}
        theosTime = {}
        for iid in self.iids:
            theos[iid] = list()
            theosTime[iid] = list()

        for event in self.events:
            if event[1] == 'Q':
                x.append(event[0])
                bid.append(event[2][0])
                ask.append(event[2][1])
                for iid in self.iids:
                    if theosNow[iid] > 0:
                        if theosNow[iid] < event[2][0] or theosNow[iid] > event[2][1]:
                            fails[iid] = fails[iid] + 1
                    else:
                        fails[iid] = fails[iid] + 1
                    pnls[iid] = pnls[iid] + calculate_pnl(event[2][0], event[2][1], theosNow[iid])

            else:
                theosTime[event[2][0]].append(event[0])
                theos[event[2][0]].append(event[2][1])
                theosNow[event[2][0]] = event[2][1]

            for iid in self.iids:
                lines[iid].set_xdata(theosTime[iid])
                lines[iid].set_ydata(theos[iid])
            plt.suptitle(self.scoreString(pnls), fontsize=14, color='red')

            plt.pause(delay)
