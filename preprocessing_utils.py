#!/usr/bin/env python3
""" 
Contains a suite of utility functions for preprocessing NLP data and VAD emotion results. 
"""

from collections import namedtuple
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag, NaiveBayesClassifier

import re, math


EmotionVAD = namedtuple('Emotion', ['V', 'A', 'D'])
# V, A and D represent Valence (negative vs. positive), 
# Arousal (calm vs. excited), and Dominance (being controlled vs. being in control)

# 8 emotions at the extreme of the cube
PROTECTED = EmotionVAD(1, -1, -1)
SATISFIED = EmotionVAD(1, -1, 1)
SURPRISED = EmotionVAD(1, 1, -1)
JOYFUL = EmotionVAD(1 ,1, 1)
SAD = EmotionVAD(-1, -1, -1)
UNCONCERNED = EmotionVAD(-1, -1, 1)
FEAR = EmotionVAD(-1, 1, -1)
ANGRY = EmotionVAD(-1, 1, 1)


BASIC_EMOTION_STRINGS = {
    PROTECTED : "Protected", 
    SATISFIED : "Satisfied", 
    SURPRISED : "Surprised", 
    JOYFUL : "Joyful", 
    SAD : "Sad", 
    UNCONCERNED : "Unconcerned", 
    FEAR : "Fear", 
    ANGRY : "Angry",
}


def closest_emotion(emotion_vad): 
    """
    Preconditions: 
        emotion_vad : EmotionVAD. The VAD values for the emotion to analyze, where each value
            has been normalized to be in the range [-1, 1].
    Returns: 
        Which of the basic emotions most resembles the VAD input values. 
    """
    min_val, min_emotion = 10, ""
    for basic_emotion in BASIC_EMOTION_STRINGS: 
        distance = _norm_between_points(basic_emotion, emotion_vad)
        if distance < min_val: 
            min_val = distance 
            min_emotion = basic_emotion

    return BASIC_EMOTION_STRINGS[min_emotion]


def preprocess_text(text): 
    """
    Preprocess the given text into tokens. This function
        - Removes stop words
        - Lemmatizes tokens
        - POS Tagging 

    Preconditions: 
        text : String. The text to preprocess. 
    Returns: 
        A list of cleaned tokens.  
    """
    # Preprocess String
    text = text.lower()
    text = text.strip()
    text = _remove_punctuation(text) 

    # Tokenize 
    tokens = word_tokenize(text)

    # Remove Stopwords + Lemmatize forms
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    cleaned_tokens = {
        lemmatizer.lemmatize(token) : True for token in tokens if not token in stop_words
    }

    return cleaned_tokens 


def _norm_between_points(emotion_vad_1, emotion_vad_2): 
    return math.sqrt(
        (emotion_vad_1.V - emotion_vad_2.V)**2 + 
        (emotion_vad_1.A - emotion_vad_2.A)**2 + 
        (emotion_vad_1.D - emotion_vad_2.D)**2
    )


def _remove_punctuation(text): 
    return re.sub(r"[^a-zA-Z0-9]+", ' ', text)
    