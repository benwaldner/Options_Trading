import pandas as pd
import numpy as np
import time
from Option import option
from Strategy import strategy
from Optimizer import optimizer

#Pull and structure AMAT data
AMATChain = pd.read_csv('./Options/AMAT.csv', header=0,
                              parse_dates=True, sep=',', dayfirst=True)
AMATChain['Days To Expiry'] = 5
AMATChain = AMATChain.head(n=4)
AMATPredictions = pd.DataFrame({"Upper Bound": 51, "Lower Bound": 48.7,
                                "Mean": 50, "Spot": 49.37}, index=[0,])
AMATPredictions['Ticker'] = 'AMAT'

#Pull and structure AAPL data
AAPLChain = pd.read_csv('./Options/AAPL.csv', header=0,
                              parse_dates=True, sep=',', dayfirst=True)
AAPLChain['Days To Expiry'] = 5
AAPLChain = AAPLChain.head(n=4)
AAPLPredictions = pd.DataFrame({"Upper Bound": 140, "Lower Bound": 134.7,
                                "Mean": 138, "Spot": 136.86}, index=[0,])
AAPLPredictions['Ticker'] = 'AAPL'

#Create one chain
optionChain = AMATChain
optionChain = AMATChain.append(AAPLChain, ignore_index=True)

#Create one prediction dataframe
predictions = AMATPredictions
predictions = predictions.append(AAPLPredictions, ignore_index=True)
print("Predictions")
print("="*25)
print(predictions)
test = strategy(optionChain, predictions)
opt = optimizer(test)
