#!/usr/bin/env python3
""" 
A script for cleaning the 1.6mil tweet sized dataset for sentiment analysis. 
"""

from bs4 import BeautifulSoup
from collections import namedtuple
from nltk.tokenize import word_tokenize

import pandas as pd 
import re

TWITTER_CSV_COLS = ['sentiment','id','date','query_string','user','text']

MENTIONS = r'@[A-Za-z0-9_]+'
HTTP_WEBSITES = r'https?://[^ ]+'
WWW_WEBSITES = r'www.[^ ]+'
NEGATIONS_DIC = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
NEG_PATTERN = re.compile(r'\b(' + '|'.join(NEGATIONS_DIC.keys()) + r')\b')


def clean_data(): 
    """
    Places a cleaned CSV file of tweets in the repo. 
    
    Cleans file by: 
        1. Dropping useless columns. 
        2. Cleaning tweet text (see below) 
    """
    # Read in .csv file, drop useless cols
    twitter_df = pd.read_csv("./trainingandtestdata/training.1600000.processed.noemoticon.csv", header=None, names=TWITTER_CSV_COLS, encoding="ISO-8859–1")
    twitter_df.drop(['id','date','query_string','user'],axis=1,inplace=True)

    # clean tweet text
    cleaned_text_tweets = []
    for i in range(len(twitter_df)): 
        cleaned_string = _tweet_cleaner(twitter_df['text'][i])
        if len(cleaned_string) > 0: 
            cleaned_text_tweets.append((cleaned_string, twitter_df['sentiment'][i]))

    # Create new DF, export to CSV 
    clean_df = pd.DataFrame(cleaned_text_tweets,columns=['text', 'sentiment'])
    clean_df['sentiment'] = twitter_df.sentiment

    clean_df.dropna(inplace=True)
    clean_df.reset_index(drop=True,inplace=True)

    clean_df.to_csv('clean_tweet.csv')

    
def _tweet_cleaner(tweet_text):
    """
    Given a text for a tweet, returns a cleaned version of the text for sentiment analysis purposes. 

    Does the following to text: 
        1. Souping
        2. BOM removing
        3. url address(‘http:’pattern), twitter ID removing
        4. url address(‘www.'pattern) removing
        5. lower-case
        6. negation handling
        7. removing numbers and special characters
        8. tokenizing and joining

    """ 
    # remove weird characters in dataset 
    soup = BeautifulSoup(tweet_text, 'lxml')
    souped = soup.get_text()

    try:
        bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
    except:
        bom_removed = souped

    # remove websites, mentions from tweets 
    removed_mentions = re.sub(MENTIONS, '', bom_removed)
    removed_websites = re.sub(HTTP_WEBSITES, '', removed_mentions)
    removed_websites = re.sub(WWW_WEBSITES, '', removed_mentions)

    cleaned_text = removed_websites.lower()

    neg_handled = re.sub(NEG_PATTERN, lambda x : NEGATIONS_DIC[x.group()], cleaned_text)
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)

    words = [x for x  in word_tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()

if __name__ == "__main__": 
    clean_data()    
