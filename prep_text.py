# Prep text

from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.parsing.preprocessing import remove_stopwords
import re 

def is_not_number(str):
    p = re.compile('^[1-9]\d*(,\d+)?$')
    r =  p.match(str)
    return False if r else True


def clean(str):
    text_no_sw = remove_stopwords(str)
    sentences = sent_tokenize(text_no_sw)
    words = word_tokenize(text_no_sw)
    words = list(filter(is_not_number, words))
    return sentences, set(words)

