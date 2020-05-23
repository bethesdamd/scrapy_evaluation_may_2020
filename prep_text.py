# Prep/clean text

from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.parsing.preprocessing import remove_stopwords
import re 
from nltk.stem.porter import PorterStemmer


def is_not_number(str):
    p = re.compile('^[1-9]\d*(,\d+)?$')
    return False if p.match(str) else True


def clean(str):
    text_no_sw = remove_stopwords(str)  # no stop words
    sentences = sent_tokenize(text_no_sw)
    tokens = word_tokenize(text_no_sw)
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in tokens]
    words = list(filter(is_not_number, stemmed))
    return sentences, set(words)  # use set() to remove duplicate words

