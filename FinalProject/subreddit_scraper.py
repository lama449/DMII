'''
Alex Lam and Maria Davis
Data Mining II final project
11/15/2020

This python file scrapes a given subreddit and gathers sentiment from reddit posts. This code has been modified to only
take posts from Apple, Amazon, Nio, and Tesla. It has been also been modified to take posts only created in 2020.

Originally Created By Patrick Richeal
'''

import util
import configparser
import praw
from psaw import PushshiftAPI
import re
import datetime
from textblob import TextBlob

# Get Configuration data
util.log('Reading config data...')
config = configparser.ConfigParser()
config.read('config.ini')

# Load symbols from symbols.txt file AAPL, AMZN, NIO, and TSLA
util.log('Loading symbols from symbols.txt...')
symbols_file = open('symbols.txt', 'r')
symbols = symbols_file.read().splitlines()
symbols_file.close()


# Find any stock symbol in given string
def get_symbol_matches(text):
    matches = []
    for symbol in symbols:
        result = re.search('[ ]+' + symbol + '[ ]+', text)
        if result != None:
            matches.append(result.group(0).strip())
    return matches


# Open symbol mentions file to write to
filename = ""
util.log('Opening ' + filename + ' file for writing to...')
symbol_mentions_file = open(filename, 'w+')

# Regex for alpha and spaces only
alpha_regex = re.compile('[^a-zA-Z ]')

# Initialize reddit sdk object with a reddit api key
util.log('Initializing reddit sdks...')
reddit = praw.Reddit(
    client_id=config['reddit']['client_id'],
    client_secret=config['reddit']['client_secret'],
    user_agent=config['reddit']['user_agent']
)
api = PushshiftAPI(reddit)


# Finds reddit posts over the target dates from 1/1/2020 to 11/13/2020
util.log('Setting up submission generator...')
start_epoch = int(datetime.datetime(2020, 1, 1).timestamp())
end_epoch = int(datetime.datetime(2020, 11, 13).timestamp())
submission_generator = api.search_submissions(subreddit='wallstreetbets', after=start_epoch, before=end_epoch)

# loop over submissions
util.log('Reading submissions for stock symbols...')
for submission in submission_generator:
    # setup search string to get symbol matches on
    search_string = ' ' + submission.title + ' ' + submission.selftext + ' '
    search_string = alpha_regex.sub(' ', search_string).lower()

    # get symbol matches using above search_string
    symbol_matches = get_symbol_matches(search_string)

    # if we got any symbol matches, get sentiment of submission title and text
    sentiment = 0
    if symbol_matches:
        textblob_obj = TextBlob(search_string)
        sentiment_val = textblob_obj.sentiment
        if sentiment_val.polarity >= 0:
            sentiment = 1
        else:
            sentiment = -1

    # for each symbol found in the content and transform epoch to month, day, and year
    for symbol in symbol_matches:
        data_string = str(datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%m/%d/%Y')) + ',' + symbol + ',' + str(sentiment)
        print(data_string)
        symbol_mentions_file.write(data_string + '\n')

# close file
symbol_mentions_file.close()
