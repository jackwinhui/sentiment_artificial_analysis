#!/usr/bin/env python3
"""
A basic sentiment analysis model leveraging the NLTK module and the EmoBank corpus.

This script
1. Preprocesses EmoBank data. 
2. Trains and Tests a Naive Bayes classifier with k-fold cross validation. 
3. Allows the user to try putting in their own sentences for the classifier. 
"""

from preprocessing_utils import closest_emotion, preprocess_text, EmotionVAD
from nltk import FreqDist, classify, NaiveBayesClassifier, MaxentClassifier

import pandas as pd 
import random

MAX_ENT_MAX_ITER = 10
NUM_DATA_PARTITIONS = 10


def preprocess_dataset(emo_df): 
    """
    Preprocesses the Pandas Dataframe for EmoBank. This function: 
    
    1. Preprocesses + Tokenizes input text.
    2. Converts VAD values to their closest basic emotion. 
    """
    dataset = []
    for ind, row in emo_df.iterrows(): 
        emotion_vad = _normalize_emobank_VAD(EmotionVAD(row['V'], row['A'], row['D']))
        emotion_label = closest_emotion(emotion_vad)

        text_tokens = preprocess_text(row['text'])

        datapoint = (text_tokens, emotion_label)
        dataset.append(datapoint)

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
            classifier = NaiveBayesClassifier.train(train_data)
        else: 
            classifier = MaxentClassifier.train(train_data, max_iter=MAX_ENT_MAX_ITER)
        accuracy = classify.accuracy(classifier, test_data)

        if accuracy > max_accuracy: 
            best_classifier = classifier
            max_accuracy = accuracy

    print(max_accuracy)
    return best_classifier


def _normalize_emobank_VAD(emotion_vad): 
    """
    Normalized EmoBank VAD values (in range [1,5]) to be in [-1, 1]. 
    """
    normalize = lambda x : (x-3)/2
    return EmotionVAD(
        normalize(emotion_vad.V), 
        normalize(emotion_vad.A),
        normalize(emotion_vad.D),
    )    


if __name__ == "__main__": 
    print("Loading EmoBank data...")
    emo_df = pd.read_csv("EmoBank/corpus/emobank.csv", index_col=0)

    print("Preprocessing EmoBank data...")
    dataset = preprocess_dataset(emo_df)

    print("Training a model...")
    classifier = k_fold_cross_validation(dataset, NUM_DATA_PARTITIONS)

    while True: 
        sentence = input("Type a sentence to try classifying: ")
        print(classifier.classify(preprocess_text(sentence)))

