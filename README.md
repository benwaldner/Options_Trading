# Options_Trading
This is a project I worked on with friends and with help from Professors at Ohio University. Initially, it was set up to take 
predictions from a machine learning model on stock prices, and find the best profit/risk scenario for weekly options, where 
risk is a certain confidence interval on the error of the model. My friends discontinued the project, but I maintained the 
optimizer as it can be used with models other than just the machine learning one. 

Methodology:

If you run main.py, you can see a brief demonstration using some old options data from the options subfolder. It reads the 2 
options chains in to pandas dataframes and uses dummy data for the predictions in another dataframe. It passes these 2 
dataframes to the strategy class, which calculates PnL on upside, downside, and expected. The strategy object is then passed 
to the optimizer class, which assigns a indicator 1 or 0 to designate taking a position in a given option. Each option is 
broken out in to long and short versions, and the optimal result is output. In the Demo folder, you can see a screenshot of 
the predicted movements, the reduced option chain, and the output.

Potential Problems:

There are a few problems that I am currently working through. The first is limiting the values to be 0 or 1, which is 
currently done to reduce the iterations required. My thoughts on this are to limit it to integers and put a max capital 
requirement as a limit, or to just simply allow fractional positions. The next problem is that by placing bounds on the 
underlying's movements, it has a tendency to create giant short strangles with breakevens out of our bounds. Another problem
is the restriction to weekly options. It runs on the assumption that we will be selling at the end of the week, essentially
at the option's intrinsic value. Position's often trade very unpredictably around this time, so the assumption may be 
unrealistic. Additionally, sometimes positions are created that have a net risk that is actually a gain, because
there's no chance of the position ending OTM in the bounds. These are ignored presently. Finally, the most glaring problem is 
the run time. The program is completely infeasible when you get more than around 12 options in a chain, especially in a speed 
driven environment. 
