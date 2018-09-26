import pandas as pd
import numpy as np
import time
from Option import option
from Strategy import strategy
from Optimizer import optimizer

#Pull and structure AMAT data
AMATChain = pd.read_csv('./Options/AMAT.csv', header=0,
                              parse_dates=True, sep=',', dayfirst=True)
print(AMATChain.head())
AMATChain['Days To Expiry'] = 5
AMATChain = AMATChain.head(n=4)
AMATPredictions = pd.DataFrame({"Upper Bound": 62, "Lower Bound": 50,
                                "Mean": 59, "Spot": 56.37}, index=[0,])
AMATPredictions['Ticker'] = 'AMAT'
print(AMATPredictions.head())
print(AMATChain.head())

#Pull and structure AAPL data
AAPLChain = pd.read_csv('./Options/AAPL.csv', header=0,
                              parse_dates=True, sep=',', dayfirst=True)
AAPLChain['Days To Expiry'] = 5
AAPLChain = AAPLChain.head(n=4)
AAPLPredictions = pd.DataFrame({"Upper Bound": 180, "Lower Bound": 165,
                                "Mean": 175, "Spot": 171.86}, index=[0,])
AAPLPredictions['Ticker'] = 'AAPL'

#Create one chain
optionChain = AMATChain
optionChain = AMATChain.append(AAPLChain, ignore_index=True)
print(optionChain.head())

#Create one prediction dataframe
predictions = AMATPredictions
predictions = predictions.append(AAPLPredictions, ignore_index=True)
print(predictions.head())

# test = strategy(optionChain, predictions)
# opt = optimizer(test)
