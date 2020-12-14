#!/usr/bin/env python3
"""
This file contains the code for creation of a GUI using PySimpleGUI to
combine sentiment analysis and event detection for analyzing journal entries
Code for GUI Source: https://github.com/israel-dryer/Notepad/blob/master/notepad.py
"""

import PySimpleGUI as sg
import pathlib
import re
from sentiment_analysis import SentimentAnalysisClassifier
from fiveWoneH import Text5W1H

sg.ChangeLookAndFeel('TanBlue')  # change style

alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


WHAT_POS_MESSAGE = "These events in your journal entry corresponded with positive moods:\n\n {}"
WHAT_NEG_MESSAGE = "These events in your journal entry corresponded with negative moods:\n\n {}"
WHO_POS_MESSAGE = "These actors in your journal entry corresponded with positive moods:\n\n {}"
WHO_NEG_MESSAGE = "These actors in your journal entry corresponded with negative moods:\n\n {}"
WHERE_POS_MESSAGE = "These places in your journal entry corresponded with positive moods:\n\n {}"
WHERE_NEG_MESSAGE = "These places in your journal entry corresponded with negative moods:\n\n {}"


WIN_W = 90
WIN_H = 25
file = None

MLINE_KEY = '-MLINE-'+sg.WRITE_ONLY_KEY


menu_layout = [['File', ['New (Ctrl+N)', 'Open (Ctrl+O)', 'Save (Ctrl+S)', 'Save As', '---', 'Exit']],
              ['Tools', ['Word Count']],
              ['Help', ['About']]]

layout = [[sg.Menu(menu_layout, text_color="white", font=('Consolas', 14))],
          [sg.Text('> Journal Entry <', font=('Consolas', 10), size=(WIN_W, 1), key='_INFO_')],
          [sg.Multiline(font=('Consolas', 12), size=(WIN_W, WIN_H), key='_BODY_')],
          [sg.Button('Analyze Text'), sg.Button('Analyze Sentiment')],
          [sg.Button('Analyze What'), sg.Button('Analyze Who'), sg.Button('Analyze Where')]]

window = sg.Window('Journal', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True, finalize=True)
window.maximize()
window['_BODY_'].expand(expand_x=True, expand_y=True)


def new_file():
    '''Reset body and info bar, and clear filename variable'''
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New File <')
    file = None
    return file


def open_file():
    '''Open file and update the infobar'''
    filename = sg.popup_get_file('Open', no_window=False)
    if filename:
        file = pathlib.Path(filename)
        window['_BODY_'].update(value=file.read_text())
        window['_INFO_'].update(value=file.absolute())
        return file


def save_file(file):
    '''Save file instantly if already open; otherwise use `save-as` popup'''
    if file:
        file.write_text(values.get('_BODY_'))
    else:
        save_file_as()


def save_file_as():
    '''Save new file or save existing file with another name'''
    filename = sg.popup_get_file('Save As', save_as=True, no_window=True)
    if filename:
        file = pathlib.Path(filename)
        file.write_text(values.get('_BODY_'))
        window['_INFO_'].update(value=file.absolute())
        return file


def word_count():
    '''Display estimated word count'''
    words = [w for w in values['_BODY_'].split(' ') if w!='\n']
    word_count = len(words)
    sg.popup_no_wait('Word Count: {:,d}'.format(word_count))


def about_me():
    '''A short, pithy quote'''
    sg.popup_no_wait('"All great things have small beginnings" - Peter Senge')


def split_into_sentences(text):
    '''
    Splitting a text into sentences
    Source: https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences
    '''
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def analyze_text():
    '''
    Final product right here baby.
    '''
    classifier = SentimentAnalysisClassifier()
    text = values.get('_BODY_')
    sentences = split_into_sentences(text)

    what_pos_answers = []
    what_neg_answers = []
    who_pos_answers = []
    who_neg_answers = []
    where_pos_answers = []
    where_neg_answers = []
    for s in sentences:
        text5w1h = Text5W1H(s)

        what = text5w1h.what()
        who = text5w1h.who()
        where = text5w1h.where()

        sentiment = classifier.classify(s)

        if what:
            what_pos_answers.append(what) if sentiment == "Positive" else what_neg_answers.append(what)
        if who:
            who_pos_answers.append(who) if sentiment == "Positive" else who_neg_answers.append(who)
        if where:
            where_pos_answers.append(where) if sentiment == "Positive" else where_neg_answers.append(where)

    message = ""
    message += (WHAT_POS_MESSAGE.format(', '.join(what_pos_answers)))
    message += "\n\n"
    
    message += (WHAT_NEG_MESSAGE.format(', '.join(what_neg_answers)))
    message += "\n\n"

    message += (WHO_POS_MESSAGE.format(', '.join(who_pos_answers)))
    message += "\n\n"

    message += (WHO_NEG_MESSAGE.format(', '.join(who_neg_answers)))
    message += "\n\n"

    message += (WHERE_POS_MESSAGE.format(', '.join(where_pos_answers)))
    message += "\n\n"

    message += (WHERE_NEG_MESSAGE.format(', '.join(where_neg_answers)))

    sg.popup_ok(message, title="Analysis")


def analyze_what():
    '''
    Extracts events from each sentence and tags them as 
    positive or negative based on sentiment_analysis methods
    based on the text found in body
    '''
    classifier = SentimentAnalysisClassifier()
    text = values.get('_BODY_')
    sentences = split_into_sentences(text)
    window['_BODY_'].update(value='')
    for s in sentences:
        answers = Text5W1H(s).what_index()
        if answers:
            start, end = answers
            sentiment = classifier.classify(s)
            color = 'green' if sentiment == 'Positive' else 'red'
            window['_BODY_'].update(value=s[:start], append=True)
            window['_BODY_'].update(value=s[start:end], background_color_for_value=color, append=True)
            window['_BODY_'].update(value=s[end:], append=True)
            window['_BODY_'].update(value=" ", append=True)
        else:
            window['_BODY_'].update(s + " ", append=True)


def analyze_who():
    '''
    Extracts events from each sentence and tags them as 
    positive or negative based on sentiment_analysis methods
    based on the text found in body
    '''
    classifier = SentimentAnalysisClassifier()
    text = values.get('_BODY_')
    sentences = split_into_sentences(text)
    window['_BODY_'].update(value='')
    for s in sentences:
        answers = Text5W1H(s).who_index()
        if answers:
            start, end = answers
            sentiment = classifier.classify(s)
            color = 'green' if sentiment == 'Positive' else 'red'
            window['_BODY_'].update(value=s[:start], append=True)
            window['_BODY_'].update(value=s[start:end], background_color_for_value=color, append=True)
            window['_BODY_'].update(value=s[end:], append=True)
            window['_BODY_'].update(value=" ", append=True)
        else:
            window['_BODY_'].update(s + " ", append=True)


def analyze_where():
    '''
    Extracts events from each sentence and tags them as 
    positive or negative based on sentiment_analysis methods
    based on the text found in body
    '''
    classifier = SentimentAnalysisClassifier()
    text = values.get('_BODY_')
    sentences = split_into_sentences(text)
    window['_BODY_'].update(value='')
    for s in sentences:
        answers = Text5W1H(s).where_index()
        if answers:
            start, end = answers
            sentiment = classifier.classify(s)
            color = 'green' if sentiment == 'Positive' else 'red'
            window['_BODY_'].update(value=s[:start], append=True)
            window['_BODY_'].update(value=s[start:end], background_color_for_value=color, append=True)
            window['_BODY_'].update(value=s[end:], append=True)
            window['_BODY_'].update(value=" ", append=True)
        else:
            window['_BODY_'].update(s + " ", append=True)


def analyze_sentiment():
    classifier = SentimentAnalysisClassifier()
    text = values.get('_BODY_')
    sentences = split_into_sentences(text)
    total = 0
    positive = 0
    for s in sentences:
        sentiment = classifier.classify(s)
        total += 1
        positive += 1 if sentiment == "Positive" else 0
    percentage = positive*100 / total
    truncate = min(4, len(str(percentage)))
    sg.popup_ok(
        "Your sentences were {}% positive.".format(str(percentage)[:truncate]), 
        title="Sentiment Analysis",
    )


def _get_answers(text):
    """
    Gets answers for each 5W1H question, if they exist.

    Return type is a map from string (e.g. 'who') to answer
    """
    results = {}
    answers = Text5W1H(text)
    who = answers.who() 
    if who:
        results['who'] = who
    what = answers.what()
    if what:
        results['what'] = what
    when = answers.when()
    if when:
        results['when'] = when
    where = answers.where()
    if where:
        results['where'] = where
    why = answers.why()
    if why: 
        results['why'] = why
    how = answers.how()
    if how:
        results['how'] = how

    return results


while True:
    event, values = window.read()
    if event in ('Exit', None):
        break
    if event in ('New (Ctrl+N)', 'n:78'):
        file = new_file()
    if event in ('Open (Ctrl+O)', 'o:79'):
        file = open_file()
    if event in ('Save (Ctrl+S)', 's:83'):
        save_file(file)
    if event in ('Save As',):
        file = save_file_as()
    if event in ('Word Count',):
        word_count()
    if event in ('About',):
        about_me()
    if event in ('Analyze Text',):
        analyze_text()
    if event in ('Analyze Sentiment',):
        analyze_sentiment()
    if event in ('Analyze What',):
        analyze_what()
    if event in ('Analyze Who',):
        analyze_who()
    if event in ('Analyze Where',):
        analyze_where()