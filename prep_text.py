# Prep/clean text

from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.parsing.preprocessing import remove_stopwords
import re 
from nltk.stem.porter import PorterStemmer


def is_not_number(str):
    p = re.compile('^[1-9]\d*(,\d+)?$')
    return False if p.match(str) else True


def clean(str):
    text = str.replace("\n", "")
    text = remove_stopwords(text)  # no stop words
    text = re.sub(r'\s{0,6}\d\s', '', text)  # removes stray numbers like '44' TODO needs improvement
    sentences = sent_tokenize(text)  
    tokens = word_tokenize(text)
    porter = PorterStemmer()
    stemmed = [porter.stem(word) for word in tokens]
    words = list(filter(is_not_number, stemmed))
    return text, sentences, set(words)  # use set() to remove duplicate words

