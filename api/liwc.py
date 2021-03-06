from py_lex import Liwc
from nltk.tokenize.casual import casual_tokenize

liwc_inst = Liwc()
liwc_inst.load('./liwc_parser.pickle')

def summarize_string(string):
    return liwc_inst.summarize_doc(casual_tokenize(string, reduce_len=True))

def annotate_string(string):
    return liwc_inst.annotate_doc(casual_tokenize(string, reduce_len=True))
