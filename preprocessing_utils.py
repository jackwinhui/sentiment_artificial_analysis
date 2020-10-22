#!/usr/bin/env python3
""" 
Contains a suite of utility functions for preprocessing NLP data and VAD emotion results. 
"""

import math
from collections import namedtuple


EmotionVAD = namedtuple('Emotion', ['V', 'A', 'D'])
# V, A and D represent Valence (negative vs. positive), 
# Arousal (calm vs. excited), and Dominance (being controlled vs. being in control)

# Ekman's Six Basic Emotions and their VAD values
ANGER = EmotionVAD(-0.43, 0.67, 0.34)
JOY = EmotionVAD(0.76, 0.48, 0.35)
SURPRISE = EmotionVAD(0.4, 0.67, -0.13)
DISGUST = EmotionVAD(-0.6, 0.35, 0.11)
FEAR = EmotionVAD(-0.64, 0.6, -0.43)
SADNESS = EmotionVAD(-0.63, 0.27, -0.33)

BASIC_EMOTION_STRINGS = {ANGER: "Anger", JOY: "Joy", SURPRISE: "Surprise", DISGUST: "Disgust", 
                        FEAR: "Fear", SADNESS: "Sadness"}


def closest_emotion(emotion_vad): 
    """
    Preconditions: 
        emotion_vad : EmotionVAD. The VAD values for the emotion to analyze, where each value
            has been normalized to be in the range [-1, 1].
    Returns: 
        Which of the six basic Ekman emotions most resembles the VAD input values. 
    """
    min_val, min_emotion = 10, ""
    for basic_emotion in BASIC_EMOTION_STRINGS: 
        distance = _norm_between_points(basic_emotion, emotion_vad)
        if distance < min_val: 
            min_val = distance 
            min_emotion = basic_emotion

    return BASIC_EMOTION_STRINGS[min_emotion]


def _norm_between_points(emotion_vad_1, emotion_vad_2): 
    """ 
    Returns: The Euclidean distance between two VAD triplets. 
    """ 
    return math.sqrt(
        (emotion_vad_1.V - emotion_vad_2.V)**2 + 
        (emotion_vad_1.A - emotion_vad_2.A)**2 + 
        (emotion_vad_1.D - emotion_vad_2.D)**2
    )

