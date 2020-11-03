#!/usr/bin/env python3
""" 
A file housing all functions for preprocessing Twitter data. 
"""

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def preprocess_text(text): 
    """
    Preprocess the given text into tokens. This function
        - Removes stop words
        - Lemmatizes tokens
    Preconditions: 
        text : String. The text to preprocess. 
    Returns: 
        The cleaned tokens, in dictionary format with all tokens mapped to True (i.e. the correct format for NLTK classifiers). 
    """
    tokens = word_tokenize(text)

    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    cleaned_tokens = {
        lemmatizer.lemmatize(token) : True for token in tokens if not token in stop_words
    }

    return cleaned_tokens
