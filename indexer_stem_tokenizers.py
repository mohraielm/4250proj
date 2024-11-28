import re
import nltk
nltk.download()
from nltk import word_tokenize

# Stemming
from nltk.stem import PorterStemmer
class StemTokenizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
    def __call__(self, doc):
        return [self.stemmer.stem(t) for t in word_tokenize(doc)]
    
from nltk.stem import WordNetLemmatizer
# Lematizer
class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

# Remove punctuation
def remove_punctuation_processor(text):
    # Remove punctuation only before or after words
    return re.sub(r'\b[.,!?;:"]+|[.,!?;:"]+\b', '', text)