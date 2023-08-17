import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
import numpy as np
import acquire


article = acquire.get_news_articles()

def prep_data(text:str, more_stopwords=[]):
    'A simple function to cleanup text data'
    wnl = nltk.stem.WordNetLemmatizer() # lemmitizer object
    # add more stop words to the original dictionary stop words from the english language
    stopwords = nltk.corpus.stopwords.words('english') + more_stopwords
    # normalize the string
    text = (unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore').lower())
    # remove not letters of numbers
    words = re.sub(r'[^\w\s]', '', text).split()
    # lemmatize the string
    lemma =  [wnl.lemmatize(word) for word in words if word not in stopwords]
    return lemma


def basic_clean(string_:list):
    clean_df = []
    for ele in string_.values:
        # Lowercase everything in the first row
        lower_str= ele.lower()
        # Normalize unicode characters
        norm_string = unicodedata.normalize("NFKD", lower_str).encode('ascii', "ignore").decode('utf-8', 'ignore')
        # Replace anything that is not a letter, number, whitespace or a single quote.
        clean_df.append(re.sub(r"[^a-z0-9'\s]", "", norm_string))
    return clean_df

normalized_str = basic_clean(article.content)

def tokenize(string_:list):
    tokenized_lst = []
    tokenizer = nltk.tokenize.ToktokTokenizer()
    for ele in string_:
        tokenized_lst.append(tokenizer.tokenize(ele, return_str=True))
    return tokenized_lst

tokenized_str = tokenize(normalized_str)

def stem(string_:list):
    # Create the nltk stemmer object, then use it
    article_stemmed_lst = []
    ps = nltk.porter.PorterStemmer()
    for parag in string_:
        stems = [ps.stem(ele) for ele in parag.split()]
        article_stemmed = " ".join(stems)
        article_stemmed_lst.append(article_stemmed)
    
    return article_stemmed_lst

stemmed_str = stem(tokenized_str)

def lemmatize(string_:list):
    # Create the nltk stemmer object, then use it
    article_lemmatize_lst = []
    wnl = nltk.stem.WordNetLemmatizer()
    for parag in string_:
        lemma = [wnl.lemmatize(ele) for ele in parag.split()]
        article_lemmatize = " ".join(lemma)
        article_lemmatize_lst.append(article_lemmatize)
    
    return article_lemmatize_lst

lemmatized_str = lemmatize(tokenized_str)

def remove_stopwords(string_:list, extra_words=None, exclude_words=None):
    article_without_stopwords = []
    # extra_words_lst = []
    for words in string_:
        stopword_list = stopwords.words('english')
        exclude_words = [w for w in words.split() if w not in stopword_list]
        # extra_words = [w for w in words.split() if w in stopword_list]

        article_without_stopwords.append(' '.join(exclude_words))
        # extra_words_lst.append(" ".join(extra_words_lst))
    return article_without_stopwords
    
removed_sp_wds = remove_stopwords(lemmatized_str)

def get_prep_data():
    article["clean_normalized"] = np.array(basic_clean(article.content))
    article["stemmed"] = np.array(stem(tokenized_str))
    article["lemmatized"] = np.array(lemmatize(tokenized_str))
    article["with_out_stop_words"] = np.array(remove_stopwords(lemmatized_str))
    return article