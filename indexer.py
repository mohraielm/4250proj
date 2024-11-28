from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from tokenizers import StemTokenizer
from database import *

def index(texts: list[str]):
    tokenizer = StemTokenizer()

    # get positions of terms from tokenizer
    term_positions = []
    for doc in texts:
        term_positions.append(tokenizer.tokenize_with_positions(doc))

    # instantiate the vectorizer object
    vectorizer = TfidfVectorizer(
        analyzer= 'word',
        strip_accents="unicode",
        stop_words=tokenizer.stemmed_stop_words,
        tokenizer=tokenizer
    )

    # build vocabulary
    vectorizer.fit(texts)

    # encode documents into vectors
    sparse_matrix = vectorizer.transform(texts)

    # retrieve the terms after tokenization, stopword removal, and stemming
    terms = vectorizer.get_feature_names_out()

    # showing the term matrix in an organized way by using a data frame
    # print("TD-IDF Vectorizer Training\n")
    # print(pd.DataFrame(data = sparse_matrix.toarray(), columns = tokens))

    inverted_index = {}

    # Iterate through every token
    for index, term in enumerate(terms):
        # Find nonzero entries for this token (documents it appears in)
        doc_indices = sparse_matrix[:, index].nonzero()[0]
        
        # Store term details in the inverted index
        inverted_index[term] = [
                {
                    "id": int(doc_id),
                    "positions": [pos for t, pos in term_positions[doc_id] if t==term],
                    "tfidf": sparse_matrix[doc_id, index]
                }
                for doc_id in doc_indices
            ]

    # Convert to DataFrame so it prints nicely in console for debugging
    inverted_index_df = pd.DataFrame([
        {"term": term, "documents": info}
        for term, info in inverted_index.items()
    ])
    print("Inverted Index\n")
    print(inverted_index_df)

    # Store each term and its info as its own document in the index collection
    for term, info in inverted_index.items():
        index_collection.update_one(
            { "_id": term },
            {"$set": {"documents": info}},  # Update or insert
            upsert=True  # Create if doesn't exist
        )