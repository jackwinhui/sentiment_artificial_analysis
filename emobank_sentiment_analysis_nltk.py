#!/usr/bin/env python3
"""
A basic sentiment analysis model leveraging the NLTK module and the EmoBank corpus.

This script
1. Preprocesses EmoBank data. 
2. Trains and Tests a Naive Bayes classifier with k-fold cross validation. 
3. Allows the user to try putting in their own sentences for the classifier. 
"""

import pandas as pd 
from preprocessing_utils import closest_emotion


def _normalize_emobank_VAD(emotion_vad): 
    """
    Normalized EmoBank VAD values (in range [1,5]) to be in [-1, 1]. 
    """
    normalize = lambda x : (x-3)/2
    return map(normalize, emotion_vad)


def preprocess_dataset(emo_df): 
    """
    Preprocesses the Pandas Dataframe for EmoBank from 


    """
    dataset = []
    for ind, row in emo_df.iterrows(): 
        emotion_vad = _normalize_emobank_VAD(Emotion(row['V'], row['A'], row['D']))
        emotion_label = closest_emotion(vad_label)

        # preprocess text 

        datapoint = (row['text'], emotion_label)
        dataset.append(datapoint)


if __name__ == "__main__": 
    print("Preprocessing EmoBank data...")
    emo_df = pd.read_csv("EmoBank/corpus/emobank.csv", index_col=0)
    print("Preprocessing EmoBank data...")
    print("Training a Naive Bayes classifier...")

    while True: 


