from typing import Literal
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from indexer_stem_tokenizers import StemTokenizer
from indexer_stem_tokenizers import LemmaTokenizer
from indexer_stem_tokenizers import remove_punctuation_processor
from database import *

def index(texts: list[str], tokenizer: Literal["Stem", "Lemma"] = "Stem"):
    if (tokenizer == "Stem"):
        tokenizer = StemTokenizer()
    elif (tokenizer == "Lemma"):
        tokenizer = LemmaTokenizer()

    # instantiate the vectorizer object
    tfidfvectorizer  = TfidfVectorizer(
        analyzer= 'word',
        strip_accents="unicode",
        stop_words='english',
        tokenizer=tokenizer,
        preprocessor=remove_punctuation_processor
    )

    # tokenize and build vocab
    tfidfvectorizer.fit(texts)

    # print all vocabulary
    print(tfidfvectorizer.vocabulary_)

    # encode documents into vectors
    training_v = tfidfvectorizer.transform(texts)

    # retrieve the terms found in the corpora
    tfidf_tokens = tfidfvectorizer.get_feature_names_out()

    # showing the term matrix in an organized way by using a data frame
    print("TD-IDF Vectorizer Training\n")
    print(pd.DataFrame(data = training_v.toarray(), columns = tfidf_tokens))