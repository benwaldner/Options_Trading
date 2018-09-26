import pandas as pd
import numpy as np
from Option import option

class strategy(object):
    #Takes pd dataframes of options and predictions
    def __init__(self, optionChain, predictions):
        self.unstructuredChain = self.buildChainNP(optionChain, predictions)
        #Builds np array of option objects
        self.structuredChain = self.buildChainPD(optionChain, predictions)

    #Create pd DF with options and calculations
    def buildChainPD(self, optionChain, predictions):
        #Loop over elements appending data to pandas DF
        for i, option in enumerate(self.unstructuredChain):
            #If its the first iteration, we need to create the DF
            if i == 0:
                chainDF = pd.DataFrame({"Ticker": option.ticker,
                                        "Strike": option.strike,
                                        "Call/Put": option.flag,
                                        "Long/Short": option.position,
                                        "Expected PnL": option.expectedPnL,
                                        "spotUpPnL": option.spotUpPnL,
                                        "spotDownPnL": option.spotDownPnL},
                                        index=[i,])
            else:
                chainDF = chainDF.append(pd.DataFrame({"Ticker": option.ticker,
                                            "Strike": option.strike,
                                            "Call/Put": option.flag,
                                            "Long/Short": option.position,
                                            "Expected PnL": option.expectedPnL,
                                            "spotUpPnL": option.spotUpPnL,
                                            "spotDownPnL": option.spotDownPnL},
                                            index=[i,]),
                                            ignore_index=True)
        return chainDF


    #Structures raw chain in format with all relevant fields for optimization
    def buildChainNP(self, optionChain, predictions):
        #Build dict containing indices of of rows matching tickers in predictions
        for index, row in predictions.iterrows():
            if index == 0:
                d = {row["Ticker"]: index}
            else:
                d[row["Ticker"]] = index

        for index, row in optionChain.iterrows():
            if index == 0:
                chain = np.array(option(row, predictions.ix[d[row["Ticker"]]], 'long'))
                chain = np.append(chain, option(row, predictions.ix[d[row["Ticker"]]], 'short'))
            else:
                chain = np.append(chain, option(row, predictions.ix[d[row["Ticker"]]], 'long'))
                chain = np.append(chain, option(row, predictions.ix[d[row["Ticker"]]], 'short'))
        return chain
