import pandas as pd
import numpy as np
from Strategy import strategy
import time

class optimizer(object):

    def __init__(self, chain):
        self.pandasChain = chain.structuredChain
        self.optimizePlay()

    #Optimization 'Engine' orchestrates flow of optimizer
    def optimizePlay(self):
        fastChain = np.array(self.pandasChain)
        bestPlay = np.zeros(np.shape(fastChain[:,0]))
        play = np.zeros(np.shape(fastChain[:,0]))
        play[0] = 1
        bestScore = 0
        while(True):
            #When this condition occurs, it means that all plays have been
            #considered
            if (play[-1] == 1) and (play[-2] == 1):
                break
            score = self.scorePlayVar(play, fastChain)
            if score > bestScore:
                bestScore = score
                bestPlay = play.copy()
            self.incrementPlay(play, 0)
        self.displayBestPlay(bestPlay)
        print "\nBest Score", bestScore
        print "\nBest Play", bestPlay

    #Used to count through plays
    def incrementPlay(self, play, index):
        #If it's a zero, increment and check for redundancies
        if play[index] == 0:
            play[index] += 1
            if (index % 2 == 0):
                self.checkForRedundancies(play, index)
        else:
            #If its a 1, then we set to 0 and increment subsequent values
            play[index] = 0
            self.incrementPlay(play, index + 1)

    #plays with 1's in even number index and index + 1 are redundant
    #ie [0, 0, 0, 1] is the same as [1, 1, 0, 1]
    def checkForRedundancies(self, play, index):
        if play[index] == 1 and play[index+1] == 1:
                self.naiveCounter(play, index)

    #Due to symmetry of binary, we can just zero out consecutive 1's to reach
    #next number in sequence. Might be redundant though, so we check
    def naiveCounter(self, play, index):
        while(play[index]):
            play[index] = 0
            index +=1
        play[index] = 1
        if index % 2 == 0:
            if (play[-2] == 0) or (play[-1] == 0):
                self.checkForRedundancies(play, index)


    def scorePlayVar(self, play, fastChain):
        #Profit first using dot product to skip calculations if negative
        profit = np.vdot(play, fastChain[:,1])
        if profit < 0:
            return 0

        #Slice fastChain to only include those where corresponding play = 1
        tempPlay = np.arange(0,np.size(fastChain[:,0]))
        tempPlay = play * tempPlay
        tempPlay = np.where(tempPlay[:] > 0)
        slicedChain = fastChain[tempPlay]

        #Get list of tickers
        tickers = np.unique(slicedChain[:,4])
        #Iterate through list of tickers getting risk associated with each
        risk = 0
        #vdot is faster than sum, so we take vector dot product to sum array
        for ticker in tickers:
            riskIndices = np.where(slicedChain[:,4] == ticker)
            coeff = np.ones(np.size(riskIndices))
            risk1 = np.vdot(coeff, slicedChain[riskIndices,5])
            risk2 = np.vdot(coeff, slicedChain[riskIndices,6])
            risk += min(risk1, risk2)

        if risk >= 0:
            return 0 #ignore nonnegative total risk for now
        return profit/abs(risk)

    # #Display options in a given play
    def displayBestPlay(self, play):
        print("\nOption Chain")
        print("="*25)
        print(self.pandasChain)
        temp = np.arange(play.size)
        temp = np.multiply(play, temp)
        temp = np.where(temp>0)[0]
        if play[0] == 1:
            temp = np.insert(temp, 0, 0)
        print("\nBest Play")
        print("="*25)
        print(self.pandasChain.loc[temp])
