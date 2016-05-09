from py_lex import EmoLex
from nltk.tokenize.casual import casual_tokenize

emo_inst = EmoLex()
emo_inst.load('./emolex_parser.pickle')

def summarize_string(string):
    return emo_inst.summarize_doc(casual_tokenize(string, reduce_len=True))

def annotate_string(string):
    return emo_inst.annotate_doc(casual_tokenize(string, reduce_len=True))
