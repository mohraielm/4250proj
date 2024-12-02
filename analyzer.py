from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from database import *
import numpy as np
import pickle

def query(query: str):
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
    query_vector = vectorizer.transform([query])

    query_text = query[0]
    non_zero_indices = query_vector.nonzero()[1].tolist()

    # Retrieve matching terms from inverted index
    matching_terms = inverted_index_collection.find({
        "pos": {"$in": non_zero_indices}
    })

    term_document_map = {}
    for term_doc in matching_terms:
        for doc in term_doc['docs']:
            doc_id = doc['id']
            position = doc['positions'][0] if doc['positions'] else None  # Handle missing positions
            if doc_id not in term_document_map:
                term_document_map[doc_id] = {'vector': {}, 'content': ""}
            term_document_map[doc_id]['vector'][term_doc['pos']] = doc['tfidf']
            term_document_map[doc_id]['position'] = position

    # Calculate cosine similarity for each document
    documents_with_cos_sim = []
    for doc_id, doc_data in term_document_map.items():
        dot_product = sum(
            query_vector[0, int(term_id)] * tfidf
            for term_id, tfidf in doc_data['vector'].items()
        )

        content_data = search_content_collection.find_one({"_id": doc_id})
        content = content_data['content'] if content_data else ""
        position = doc_data['position']
        if position is None:
            print(f"Warning: 'position' is None for document with content: {content[:50]}")
            start_pos = 0
            end_pos = min(200, len(content))  # Default to the first 200 characters
        else:
            # Get 100 characters before and after the position
            start_pos = max(0, position - 100)
            end_pos = min(len(content), position + 100)

        highlighted_content = content[start_pos:end_pos]
        documents_with_cos_sim.append({
            "url": doc_id,
            "content": highlighted_content,
            "cosine_similarity": dot_product
        })

    # Sort documents by cosine similarity first, then by position (closer positions rank higher)
    documents_with_cos_sim.sort( key=lambda x: -x['cosine_similarity'] )

    # Display results for the query
    documents_with_cos_sim

    return documents_with_cos_sim
