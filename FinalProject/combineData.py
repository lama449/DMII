'''
Alex Lam and Maria Davis
Data Mining II final project
11/15/2020

This python file will combine data collected from the subreddit scraper and the NASDAQ dataset.
'''

import pandas as pd

# Load the data collected from the scraper
redditdata = pd.read_csv('stocks.csv')

# Create a count for the number of posts given for a particular day
redditdata['Count'] = redditdata.groupby(['Date', 'Stock']).transform('count')

# Create a continuous sentiment based on the number of posts created for a particular day
reddit_sent = redditdata.groupby(['Date', 'Stock']).agg({'Date': 'first', 'Stock': 'first',
                                                         'Sentiment': 'mean', 'Count': 'first'}).reset_index(drop=True)

# Create the dataset for TSLA
historical_tsla = pd.read_csv('HistoricalTSLA.csv')
historical_tsla = historical_tsla[['Date', 'Direction']]
reddit_tsla_sent = reddit_sent[reddit_sent['Stock'] == 'tsla']

# Create the dataset for AAPL
historical_aapl = pd.read_csv('HistoricalAAPL.csv')
historical_aapl = historical_aapl[['Date', 'Direction']]
reddit_aapl_sent = reddit_sent[reddit_sent['Stock'] == 'aapl']

# Create the dataset for AMZN
historical_amzn = pd.read_csv('HistoricalAMZN.csv')
historical_amzn = historical_amzn[['Date', 'Direction']]
reddit_amzn_sent = reddit_sent[reddit_sent['Stock'] == 'amzn']

# Create the dataset for NIO
historical_nio = pd.read_csv('HistoricalNIO.csv')
historical_nio = historical_nio[['Date', 'Direction']]
reddit_nio_sent = reddit_sent[reddit_sent['Stock'] == 'nio']

# Combines the sentiment data with the Nasdaq data for the overall dataset.
output_tsla = pd.merge(historical_tsla, reddit_tsla_sent, on='Date')
output_aapl = pd.merge(historical_aapl, reddit_aapl_sent, on='Date')
output_amzn = pd.merge(historical_amzn, reddit_amzn_sent, on='Date')
output_nio = pd.merge(historical_nio, reddit_nio_sent, on='Date')

output_tsla.to_csv('stockstsla.csv')
output_aapl.to_csv('stocksaapl.csv')
output_amzn.to_csv('stocksamzn.csv')
output_nio.to_csv('stocksnio.csv')
