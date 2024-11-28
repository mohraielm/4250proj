from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from tokenizers import StemTokenizer
from database import *

def index(documents: Dict[str, str]):
    tokenizer = StemTokenizer()
    texts = list(documents.values())

    # get positions of terms from tokenizer
    term_positions = []
    for text in texts:
        term_positions.append(tokenizer.tokenize_with_positions(text))

    # instantiate the vectorizer object
    vectorizer = TfidfVectorizer(
        analyzer= 'word',
        strip_accents="unicode",
        stop_words=tokenizer.stemmed_stop_words,
        tokenizer=tokenizer
    )

    # build vocabulary
    vectorizer.fit(texts)

    # store vocabulary in vocabulary collection to reinitialize TfidVectorizer for querying later
    vocabulary_collection.update_one(
        { "_id": "vocabulary_doc" },  # manually set _id so that we can overwrite this doc
        { "$set": { "vocabulary": vectorizer.vocabulary_.copy() } },   # Note: use a copy of the vocabulary list otherwise MongoDB can directly mutate the original vocabulary
        upsert=True
    )

    # encode documents into vectors
    sparse_matrix = vectorizer.transform(texts)

    # map urls to sparse_vectors
    url_to_sparse_vector = {}

    for i, url in enumerate(documents.keys()):
        url_to_sparse_vector[url] = sparse_matrix[i]

    # store vector for each document in index collection
    # iterate through each document
    for doc_index, (url, _) in enumerate(documents.items()):
        sparse_vector = sparse_matrix[doc_index]

        # convert sparse_vector into a dictionary so we can directly insert into a mongodb document
        indices = [str(term_index) for term_index in sparse_vector.indices]   # converts np.int32 indices into strings to be used as mongoDB fields
        values = sparse_vector.data
        sparse_vector_to_dict = dict(zip(indices, values))

        # store sparse vector and doc id in mongodb index collection
        index_collection.update_one(
            { "_id": url },
            { "$set": { "sparseVector": sparse_vector_to_dict } },
            upsert=True  # Create if doesn't exist
        )


    # retrieve the terms after tokenization, stopword removal, and stemming
    terms = vectorizer.get_feature_names_out()

    # Print term matrix using a dataframe for console print formatting
    print("TD-IDF Vectorizer Training\n")
    print(pd.DataFrame(data = sparse_matrix.toarray(), columns = terms))

    inverted_index = {}

    # Iterate through every token
    for doc_index, (url, _) in enumerate(documents.items()):
        sparse_vector = sparse_matrix[doc_index]
        
        # Iterate through each nonzero entry in the sparse vector
        for term_index, term in enumerate(terms):
            # If this term appears in the current document
            if term_index in sparse_vector.indices:
                tfidf = sparse_vector.data[sparse_vector.indices == term_index][0]

                # Add the term to the inverted index
                if term not in inverted_index:
                    inverted_index[term] = []

                inverted_index[term].append({
                    "id": url,
                    "positions": [pos for t, pos in term_positions[doc_index] if t == term],  # Get term positions
                    "tfidf": tfidf
                })

    # Print inverted index using a dataframe for console print formatting
    inverted_index_df = pd.DataFrame([
        {"term": term, "documents": info}
        for term, info in inverted_index.items()
    ])
    print("Inverted Index\n")
    print(inverted_index_df)

    # Store each term and its info as its own document in the index collection
    for term, info in inverted_index.items():
        inverted_index_collection.update_one(
            { "_id": term },
            { "$set": { "documents": info } },
            upsert=True  # Create if doesn't exist
        )