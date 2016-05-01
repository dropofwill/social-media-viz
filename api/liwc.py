from py_lex import Liwc
from nltk.tokenize.casual import casual_tokenize

liwc_inst = Liwc()
liwc_inst.load('./liwc_parser.pickle')

def get_liwc_instance(pickle_path='./liwc_parser.pickle'):
    l = Liwc()
    l.load(pickle_path)
    return l

def summarize_string(string):
    return liwc_inst.summarize_doc(casual_tokenize(string, reduce_len=True))
