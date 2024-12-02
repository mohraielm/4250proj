from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from database import *
import numpy as np
import pickle

def query(queries: list):
    '''
    Queries the indexed data to find matching documents with cosine similarity.

    Args:
        queries: List of query strings to search for.

    Returns:
        A dictionary with queries as keys and a list of matching documents with cosine similarity scores as values.
    '''
    # Load vocabulary from the database
 
    vectorizer_document = vectorizer_collection.find_one({"_id": "vectorizer_doc"})
    serialized_vectorizer = vectorizer_document["vectorizer"] 
    vectorizer: TfidfVectorizer = pickle.loads(serialized_vectorizer)  

    # Transform queries into vectors
    query_vectors = vectorizer.transform(queries)
    results = {}

    for query_index, query_vector in enumerate(query_vectors):
        query_text = queries[query_index]
        non_zero_indices = query_vector.nonzero()[1].tolist()

        # Retrieve matching terms from inverted index
        matching_terms = inverted_index_collection.find({
            "pos": {"$in": non_zero_indices}
        })

        term_document_map = {}
        for term_doc in matching_terms:
            for doc in term_doc['docs']:
                doc_id = doc['id']
                if doc_id not in term_document_map:
                    term_document_map[doc_id] = {'vector': {}, 'content': ""}
                term_document_map[doc_id]['vector'][term_doc['pos']] = doc['tfidf']

        # Calculate cosine similarity for each document
        documents_with_cos_sim = []
        for doc_id, doc_data in term_document_map.items():
            dot_product = sum(
                query_vector[0, int(term_id)] * tfidf
                for term_id, tfidf in doc_data['vector'].items()
            )
            documents_with_cos_sim.append({
                "content": documents_collection.find_one({"_id": doc_id})['content'],
                "cosine_similarity": dot_product
            })

        # Sort documents by similarity
        documents_with_cos_sim.sort(key=lambda x: x['cosine_similarity'], reverse=True)
        results[query_text] = documents_with_cos_sim

    return results
