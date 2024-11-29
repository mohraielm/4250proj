import re
import nltk
# nltk.download() # uncomment to download stopword and tokenize libraries
from nltk import word_tokenize
from nltk.corpus import stopwords

# Stemming
from nltk.stem import PorterStemmer
class StemTokenizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.term_positions = []

    def tokenize(self, doc):
        '''
        Hijack tokenization flow so that we can calculate char positions of a token based on the original text

        Args:
            doc: original text of a document of type string
        Returns:
            stemmed_tokens: a list of stemmed tokens based on the original text
        '''
        text = remove_punctuation_processor(doc)
        tokens = word_tokenize(text)  # Tokenize the text

        term_positions = {}
        stemmed_tokens = []

        for token in tokens:
            if (token.lower() not in self.stop_words):  # Check if token is a stop_word
                stemmed_token = self.stemmer.stem(token)  # Stem the token
                stemmed_tokens.append(stemmed_token)

                if stemmed_token not in term_positions:
                    positions = self.getTokenPositions(token, doc)
                    term_positions[stemmed_token] = positions

        self.term_positions.append(term_positions)
        return stemmed_tokens
    
    def getTokenPositions(self, token, doc):
        '''
        Calculates a token's char positions based on the original text

        Args:
            token: token to calculate the char positions for
            doc: original text of a document of type string
        '''
        positions = []
        matches = re.finditer(token, doc)

        for match in matches:
            positions.append(match.start())

        return positions
    
    # Function that is called by the TfidVectorizer for every document
    def __call__(self, doc):
        return self.tokenize(doc)

# Remove punctuation
def remove_punctuation_processor(text):
    # Remove punctuation only before or after words
    return re.sub(r'\b[.,!?;:"]+|[.,!?;:"]+\b', '', text)