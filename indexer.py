from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from tokenizers import StemTokenizer
import pickle
from database import *

def index(documents: Dict[str, str]):
    '''
    Creates/updates three collections in the database:\n
    vocabualary: stores all terms and their indices,\n
    index: stores a vector for each document id'd by their url,\n
    invertedIndex: stores every document and tfidf value that has that term in its text

    Args:
        documents: a map representation of document url's and their text to index.\nExample: { 'https://testurl.com/relative-path': 'Text of the document goes here' }
    '''
    tokenizer = StemTokenizer()
    texts = list(documents.values())

    # instantiate the vectorizer object
    vectorizer = TfidfVectorizer(
        analyzer= 'word',
        strip_accents="unicode",
        tokenizer=tokenizer
    )

    # build vocabulary
    vectorizer.fit(texts)

    serialized_vectorizer = pickle.dumps(vectorizer)
    vectorizer_collection.update_one(
        { "_id": "vectorizer_doc" },
        { "$set": { "vectorizer": serialized_vectorizer } },
        upsert=True
    )

    # encode documents into vectors
    sparse_matrix = vectorizer.transform(texts)

    # map urls to sparse_vectors
    url_to_sparse_vector = {}

    for i, url in enumerate(documents.keys()):
        url_to_sparse_vector[url] = sparse_matrix[i]

    # Adding pos field for inverted index
    vocabulary = vectorizer.vocabulary_
    inverted_index = {}
    for term, pos in vocabulary.items():
        inverted_index[term] = {"_id": pos, "pos": pos, "docs": []}

    # Iterate through every token
    for doc_index, (url, _) in enumerate(documents.items()):
        sparse_vector = sparse_matrix[doc_index]

        # Iterate through each nonzero entry in the sparse vector
        for term, pos in vocabulary.items():
            # If this term appears in the current document
            if pos in sparse_vector.indices:
                tfidf = sparse_vector[0, pos]

                # Add the term to the inverted index
                inverted_index[term]["docs"].append({
                    "id": url,
                    "positions": [pos for pos in tokenizer.term_positions[doc_index][term]],  # Get term positions
                    "tfidf": tfidf})
                
    # Store each term and its info as its own document in the index collection
    for term, info in inverted_index.items():
        inverted_index_collection.update_one(
            { "_id": term },
            { "$set": { 
                "pos": info['pos'],
                "docs": info['docs']
            }},
            upsert=True  # Create if doesn't exist
        )