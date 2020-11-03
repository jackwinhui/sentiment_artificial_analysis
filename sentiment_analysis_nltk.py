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
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd 
import random

MAX_ENT_MAX_ITER = 10
NUM_DATA_PARTITIONS = 10

CSV_FILE_NAME = "clean_tweet.csv"


def preprocess_dataset(): 
    """
    Preprocesses the cleaned twitter CSV file for training/testing on NLTK. 
    
    1. Preprocesses + Tokenizes input text.
    2. Converts VAD values to their closest basic emotion. 
    3. Prints TFIDF (and does nothing else with it). 
    """
    tweet_df = pd.read_csv(CSV_FILE_NAME, index_col=0, encoding='ISO-8859–1', na_filter=False)

    dataset = []
    strs = [] 

    for ind, row in tweet_df.iterrows(): 
        sentiment_label = row['sentiment']
        text_tokens = preprocess_text(row['text'])

        strs.append(row['text'])

        datapoint = (text_tokens, sentiment_label)
        dataset.append(datapoint)

    tf_idf = TfidfVectorizer(tokenizer=preprocess_text, stop_words='english')
    tds = tf_idf.fit_transform(strs)

    print(tds)
    return dataset 


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
    print("Preprocessing Twitter data...")
    dataset = preprocess_dataset()

    print("Training a model...")
    classifier = k_fold_cross_validation(dataset, NUM_DATA_PARTITIONS)

    while True: 
        sentence = input("Type a sentence to try classifying: ")
        labeler = lambda x : "Positive" if x > 0 else "Negative"
        print(labeler(classifier.classify(preprocess_text(sentence))))

