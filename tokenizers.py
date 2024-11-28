import re
import nltk
# nltk.download()
from nltk import word_tokenize
from nltk.corpus import stopwords

# Stemming
from nltk.stem import PorterStemmer
class StemTokenizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stemmed_stop_words = [self.stemmer.stem(word) for word in stopwords.words('english')]

    def tokenize(self, doc):
        text = remove_punctuation_processor(doc)
        tokens = word_tokenize(text)  # Tokenize the text
        stemmed_tokens = []
        
        # Iterate through tokens and track token index
        for token in tokens:
            stemmed_token = self.stemmer.stem(token)  # Stem the token
            stemmed_tokens.append(stemmed_token)

        return stemmed_tokens
    
    def __call__(self, doc):
        return self.tokenize(doc)

# Remove punctuation
def remove_punctuation_processor(text):
    # Remove punctuation only before or after words
    return re.sub(r'\b[.,!?;:"]+|[.,!?;:"]+\b', '', text)