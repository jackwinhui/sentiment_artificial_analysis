# Sentiment Artificial Analysis

This repo contains the Cornell NLP 4701 (AI Practicum) project by Jackwin Hui, Joe Choi, John Guo. 

## Goals 

Today, young adults more than ever struggle with reflecting on the causes of their own emotions. Through this project, we aim to help users understand themselves by providing them with objective information about the way they are responding to events around them. The user will input journal entries into our platform, and our product will output an analysis of events and emotions from this journal entry. For example, if a user enters a week’s worth of journal entries onto our platform, our product might tell the user something like “We found that on 5 out of 7 days last week, you were stressed due to schoolwork”.

## Setup 

First, follow Python virtual environment setup here:  https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3 

Then, to install dependencies using pip, navigate to this repo in your commmand line and run: 

```
pip install -r requirements.txt
```

Finally, to install NLTK requirements, run the following from the command line: 

```
python3 nltk_downloads.py
```

## Training + Testing the Models

To run the code from the starter project, performing a simple Positive/Negative sentiment analysis on NLTK's built in Twitter dataset, run: 
```
python3 nlp_test.py
```

First, to create a cleaned .csv file for the Twitter Dataset, run: 
```
python3 clean_twitter_csv.py
```

To run the NTLK-based classifier for 8 different emotions on the EmoBank corpus, run: 
```
python3 sentiment_analysis.py
```

1,600,000 entry data set from twitter download link:
http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip 

## Running 5W1H 
Note that to use any methods from the `Text5W1H` class, you will have to start the core-nlp server first from the command line. This can be done by running the following from the command line. 
```
giveme5w1h-corenlp
```

## References
* Sven Buechel and Udo Hahn. 2017. EmoBank: Studying the Impact of Annotation Perspective and Representation Format on Dimensional Emotion Analysis. In EACL 2017 - Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics. Valencia, Spain, April 3-7, 2017. Volume 2, Short Papers, pages 578-585. Available: http://aclweb.org/anthology/E17-2092
* Sven Buechel and Udo Hahn. 2017. Readers vs. writers vs. texts: Coping with different perspectives of text understanding in emotion annotation. In LAW 2017 - Proceedings of the 11th Linguistic Annotation Workshop @ EACL 2017. Valencia, Spain, April 3, 2017, pages 1-12. Available: https://sigann.github.io/LAW-XI-2017/papers/LAW01.pdf
* Ricky Kim. 2018. Personal project on sentiment analysis using twitter datasets. Available: https://towardsdatascience.com/another-twitter-sentiment-analysis-with-python-part-11-cnn-word2vec-41f5e28eda74 
* @InProceedings{Hamborg2019b,
  author    = {Hamborg, Felix and Breitinger, Corinna and Gipp, Bela},
  title     = {Giveme5W1H: A Universal System for Extracting Main Events from News Articles},
  booktitle = {Proceedings of the 13th ACM Conference on Recommender Systems, 7th International Workshop on News Recommendation and Analytics (INRA 2019)},
  year      = {2019},
  month     = {Sept.},
  location  = {Copenhagen, Denmark}
}




