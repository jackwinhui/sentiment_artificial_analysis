#!/usr/bin/env python3
"""
A basic sentiment analysis model leveraging the NLTK module and the EmoBank corpus.

This script:
    1. Preprocesses EmoBank data. 
    2. Trains and Tests a Naive Bayes classifier with k-fold cross validation. 
    3. Allows the user to try putting in their own sentences for the classifier. 

Results: With k=10, n=10000+, we found that
    - Naive Bayes Classifier gave us ~24% accuracy
    - Max Entropy Classifier gave us ~27% accuracy
"""

from preprocessing_utils import preprocess_text
from nltk import FreqDist, classify, NaiveBayesClassifier, MaxentClassifier, SklearnClassifier
from nltk.text import TextCollection
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import pandas as pd 
import numpy as np
import random

MAX_ENT_MAX_ITER = 10
NUM_DATA_PARTITIONS = 10
SEED = 2000

CSV_FILE_NAME = "clean_tweet.csv"
TWEET_DF = pd.read_csv(CSV_FILE_NAME, index_col=0, encoding='ISO-8859–1', na_filter=False)


def johns_pipeline(tweet_df): 
    """
    Returns: pipeline 
    """
    classifier = LogisticRegression()

    """
    #TFIDF Vectorizer
    tf_idf = TfidfVectorizer(tokenizer=preprocess_text, stop_words='english')
    tds = tf_idf.fit_transform(strs)
    """
    #Count Vectorizer 
    count_v = CountVectorizer(max_features=80000, ngram_range=(3, 3)) #trigrams with 80,000 features
    count_v_matrix = count_v.fit_transform(tweet_df.text)

    #Pipeline
    pipeline = Pipeline([('vectorizer', count_v), ('classifer', classifier)])

    return pipeline 

def cross_validation(pipeline, tweet_df):
    x = tweet_df.text
    y = tweet_df.sentiment
    x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=.02, random_state=SEED)

    classifier = pipeline.fit(x_train, y_train)
    y_pred = classifier.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: {}".format(accuracy))
    return classifier

def k_fold_cross_validation(dataset, k, classifier_type="naive_bayes"):
    """ 
    Creates a classifier via K-Fold cross validation. 
    """ 
    random.shuffle(dataset)
    max_accuracy = 0.0
    best_classifier = None

    partition_size = len(dataset) // k

    for i in range(k): 
        test_start = i*partition_size
        test_end = (i+1)*partition_size

        test_data = dataset[test_start:test_end]
        train_data = dataset[:test_start] + dataset[test_end:]

        if classifier_type == "naive_bayes": 
            sk_classifier = SklearnClassifier(MultinomialNB())
            classifier = sk_classifier.train(train_data)
        else: 
            classifier = MaxentClassifier.train(train_data, max_iter=MAX_ENT_MAX_ITER)
        accuracy = classify.accuracy(classifier, test_data)

        if accuracy > max_accuracy: 
            best_classifier = classifier
            max_accuracy = accuracy

    print("K-fold cross validation's best accuracy was " + str(max_accuracy) + ".")
    return best_classifier


def _create_tf_idf(source): 
    """ 
    An attempt to create an NLTK text collection object. 
    """ 
    tf_idf = TfidfVectorizer(tokenizer=preprocess_text, stop_words='english')
    tfs = tf_idf.fit_transform(source.keys())
    print(tf_idf.get_feature_names())
    return tfs


if __name__ == "__main__": 

    classifier = cross_validation(johns_pipeline(TWEET_DF), TWEET_DF)

    while True: 
        sentence = input("Type a sentence to try classifying: ")
        labeler = lambda x : "Positive" if x > 0 else "Negative"
        print(labeler(classifier.predict(sentence)))

