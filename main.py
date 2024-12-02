from database import *
from indexer import index
from analyzer import query

while True:
    print("\nMenu:")
    print("1. Crawl")
    print("2. Parse")
    print("3. Index")
    print("4. Query")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("Option 1 selected")
    elif choice == "2":
        print("Option 2 selected")
    elif choice == "3":
        # get search content to index
        search_content = search_content_collection.find()
        search_content_list = {}

        for content in search_content:
            search_content_list[content['_id']] = content['content']

        # pass in an array of strings to index
        index(search_content_list) # UNCOMMENT TO USE INDEXER
    elif choice == "4":
        user_query = input("Enter your query: ")

        results = query([user_query])

        # Display results
        for query, docs in results.items():
            print(f"Query: {query}")

    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
