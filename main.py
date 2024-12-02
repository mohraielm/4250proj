from database import *
from indexer import index
from crawler import crawler
from parser import parser
from analyzer import query
import math

BOLD = '\033[1m'
PURPLE = '\033[95m'
BLUE = '\033[34m'
RESET = '\033[0m'
CLEAR = '\033c'

def pagination(results: list):
    page = 1
    while True:
        print(CLEAR, end='')
        print(f'{BOLD}{PURPLE}-----{len(results)} Results-----{RESET}')
        for i in range(page*5 - 5, page*5):
            if (i >= len(results)):
                continue
            result = results[i]
            print(f'{BLUE}{result["url"]}{RESET}')
            print(f'...{result["content"]}...')
            print()
        print(f'{BOLD}{PURPLE}Page {page} of {math.ceil(len(results) / 5)}{RESET}')
        
        print('Menu:')
        print('1. Previous')
        print('2. Next')
        print('3. Return to Main Menu')
        choice = input("Enter your choice: ")

        if choice == "1":
            page -= 1
            if (page < 1):
                page = 1
        elif choice == "2":
            page += 1
            if (page > math.ceil(len(results) / 5)):
                page -= 1
        elif choice == "3":
            break

while True:
    print(CLEAR, end='')
    print("\nMenu:")
    print("1. Crawl")
    print("2. Parse")
    print("3. Index")
    print("4. Query")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        crawler('https://www.cpp.edu/engineering/ce/index.shtml')
    elif choice == "2":
        # find the target documents in the pages collection
        targets = pages_collection.find({'isTarget': True})

        # pass in cursor object to parser
        parser(targets)
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
        results = query(user_query)
        pagination(results)

    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")