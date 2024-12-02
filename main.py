from database import *
from indexer import index
from analyzer import query 

# crawl
# from crawler import *     # UNCOMMENT TO USE CRAWLER
# parse
# from parser import *      # UNCOMMENT TO USE PARSER

# get search content to index
search_content = search_content_collection.find()
search_content_list = {}

for content in search_content:
    search_content_list[content['_id']] = content['content']

# pass in an array of strings to index
# index(search_content_list) # UNCOMMENT TO USE INDEXER

# Run queries
queries = ["machine learning", "research activities", "Deep Learning"]
results = query(queries)

# Display results
for query, docs in results.items():
    print(f"Query: {query}")
    for doc in docs:
        print(f"  Content: {doc['content']}\n  Similarity: {doc['cosine_similarity']:.2f}")
