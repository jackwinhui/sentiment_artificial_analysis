#!/usr/bin/env python3
"""
This file is a scikit-learn based module for testing/training
a sentiment analysis model based on the 1.6m twitter dataset
from Stanford. This file currently:

1. Creates an sklearn pipeline for training/testing.
2. Trains/tests on this pipeline + the twitter dataframe.

"""

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd

SEED = 2000

CSV_FILE_NAME = "clean_tweet.csv"
TWEET_DF = pd.read_csv(
    CSV_FILE_NAME, index_col=0, encoding='ISO-8859–1', na_filter=False
)


def sklearn_pipeline(tweet_df, max_features, ngram_range):
    """
    Given the twitter dataframe, returns a SKLearn Pipeline to vectorize
    and classify data. This pipeline uses a count vectorizer with
    a Logistic Regression based classifier.

    Parameters:
        tweet_df : The pandas dataframe for the twitter object.
        max_features : The maximum number of features for the count vectorizor.
        ngram_range : a tuple (a,b), where a is the minimum n-grams size to try
            and b is the max n-grams size to try.

    Returns: A SKLearn pipeline for cross validation.
    """
    classifier = LogisticRegression()

    """
    TODO: Leverage TFIDF in the pipeline.

    # TFIDF Vectorizer
    tf_idf = TfidfVectorizer(tokenizer=preprocess_text, stop_words='english')
    tds = tf_idf.fit_transform(strs)
    """

    # Count Vectorizer
    count_v = CountVectorizer(
        max_features=max_features,
        ngram_range=ngram_range
    )
    # count_v_matrix = count_v.fit_transform(tweet_df.text) # unused

    # Pipeline
    pipeline = Pipeline([('vectorizer', count_v), ('classifer', classifier)])

    return pipeline


def train_and_test(pipeline, tweet_df, test_size):
    """
    Given an sklearn pipeline, randomly split the twitter
    data given the test_size. Then, train a classifier with
    the pipeline, and test said classifier, and return the
    accuracy.

    Parameters:
        pipeline. An sklearn pipeline to use for train/test.
        tweet_df. The twitter dataframe of data.
        test_size. A number between 0 and 1, indicating what percentage
            of the data should be used for testing.
    Returns:
        classifier, accuracy. The classifier and its accuracy score.
    """
    # TODO: Implement cross-validation
    x = tweet_df.text
    y = tweet_df.sentiment
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=test_size, random_state=SEED
    )

    classifier = pipeline.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    return classifier, accuracy


if __name__ == "__main__":
    # Trigrams with 80000 max features
    print("Creating scikit-learn pipeline...")
    pipeline = sklearn_pipeline(
        tweet_df=TWEET_DF,
        max_features=80000,
        ngram_range=(3, 3),
    )
    # Train/Test with .02 test split
    print("Training + testing classifier...")
    classifier, accuracy = train_and_test(
        pipeline=pipeline,
        tweet_df=TWEET_DF,
        test_size=.02,
    )

    print("Created a classifier with accuracy of {}".format(accuracy))

    while True:
        sentence = input("Type a sentence to try classifying: ")
        print("Positive" if classifier.predict([sentence]) > 0 else "Negative")
