import pandas as pd
import numpy as np

class option(object):

    'Takes 2 pandas series objects, option positioning as arguments'
    def __init__(self, optionChain, predictions, longShort):
        'optionChain Info'
        self.ticker = optionChain["Ticker"]
        self.bid = optionChain["Bid"]
        self.ask = optionChain["Ask"]
        self.flag = optionChain["Flag"]
        self.expiry = optionChain["Days To Expiry"]
        self.strike = optionChain["Strike"]
        self.position = longShort

        'Prediction Info'
        self.maxSpot = predictions["Upper Bound"]
        self.minSpot = predictions["Lower Bound"]
        self.expectedSpot = predictions["Mean"]
        self.underlying = predictions["Spot"]

        'Calculated parameters'
        self.expectedPnL = self.getExpectedPnL()
        self.spotUpPnL = self.getSpotUpPnL()
        self.spotDownPnL = self.getSpotDownPnL()

    #Calculate PnL based on predicted underlying level at expiry
    def getExpectedPnL(self):
        if self.position == 'long':
            if self.flag == 'c':
                return max(self.expectedSpot - self.strike,0) - self.ask
            else:
                return max(self.strike - self.expectedSpot,0) - self.ask
        else:
            if self.flag == 'c':
                return self.bid - max(self.expectedSpot - self.strike,0)
            else:
                return self.bid - max(self.strike - self.expectedSpot,0)

    #Calculate PnL based on max underlying level at expiry
    def getSpotUpPnL(self):
        if self.position == 'long':
            if self.flag == 'c':
                return max(self.maxSpot - self.strike,0) - self.ask
            else:
                return max(self.strike - self.maxSpot,0) - self.ask
        else:
            if self.flag == 'c':
                return self.bid - max(self.maxSpot - self.strike,0)
            else:
                return self.bid - max(self.strike - self.maxSpot,0)

    #Calculate PnL based on min underlying level at expiry
    def getSpotDownPnL(self):
        if self.position == 'long':
            if self.flag == 'c':
                return max(self.minSpot - self.strike,0) - self.ask
            else:
                return max(self.strike - self.minSpot,0) - self.ask
        else:
            if self.flag == 'c':
                return self.bid - max(self.minSpot - self.strike,0)
            else:
                return self.bid - max(self.strike - self.minSpot,0)

    def displayOption(self):
        print "\n"
        print self.ticker, self.strike, self.position, self.flag
        print "=================================================="
        print "Bid:\t\t\t|$",self.bid
        print "Ask:\t\t\t|$",self.ask
        print "Days to Mature:\t\t|",self.expiry
        print "Expected to make:\t|$",self.expectedPnL
        print "PnL on Upside:\t\t|$",self.spotUpPnL
        print "PnL on Downside:\t|$",self.spotDownPnL
