import re
import nltk
nltk.download()
from nltk import word_tokenize
from nltk.corpus import stopwords

# Stemming
from nltk.stem import PorterStemmer
class StemTokenizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stemmed_stop_words = [self.stemmer.stem(word) for word in stopwords.words('english')]

    def tokenize_with_positions(self, doc):
        text = remove_punctuation_processor(doc)
        tokens = word_tokenize(text)  # Tokenize the text
        stemmed_tokens_with_positions = []
        
        # Iterate through tokens and track token index
        for token_index, token in enumerate(tokens):
            stemmed_token = self.stemmer.stem(token)  # Stem the token
            stemmed_tokens_with_positions.append((stemmed_token, token_index))  # Append tuple

        return stemmed_tokens_with_positions
    
    def __call__(self, doc):
        return [token for token, _ in self.tokenize_with_positions(doc)]

# Remove punctuation
def remove_punctuation_processor(text):
    # Remove punctuation only before or after words
    return re.sub(r'\b[.,!?;:"]+|[.,!?;:"]+\b', '', text)