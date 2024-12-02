import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
from database import *

def crawler(seed_url: str):
    # initialize frontier
    frontier = deque()
    frontier.append(seed_url)

    # initialize set for visited links
    visited = set()

    NUMBER_TARGETS = 10

    # define re for easier access to expression
    relative_url = r'^\/(?!\/)' 
    cpp_base = "https://www.cpp.edu/"

    # initialize counter for number of targets
    targets_found = 0

    while frontier:
        # get the next URL from the queue
        url = frontier.popleft()
        
        try:
            html = urlopen(url)
            data = html.read()
        except Exception as e:
            print(f"{url} {e}")
            continue

        content_type = html.info().get_content_type()

        if 'html' not in content_type:
            continue

        bs = BeautifulSoup(data, 'html.parser')

        # check if target is found (header is found)
        target = bs.find('div', {'class': 'fac-info'})
        if target:
            pages_collection.update_one(
                { '_id': url },
                { '$set': {
                    'content': data.decode('utf-8'),
                    'isTarget': True
                }},
                upsert = True
            )
            targets_found += 1

            # check if number_targets is reached
            if targets_found >= NUMBER_TARGETS:
                break
        else:
            pages_collection.update_one(
                { '_id': url },
                { '$set': { 'content': data.decode('utf-8') } },
                upsert = True
            )

            raw_links = [link['href'] for link in bs.find_all('a', href=True)]

            linked_urls = []
            for url in raw_links:
                url = url.strip()

                if url.endswith('/'):
                    url = url[:-1]
                
                if re.match(relative_url, url):
                    # clean / in beginning of relative url
                    if url.startswith('/'):
                        url = cpp_base + url[1:]
                    
                    elif url.startswith('~'):
                        url = cpp_base + url[1:]

                if url.startswith(cpp_base) and url not in visited:
                    linked_urls.append(url)

            for url in set(linked_urls):
                if url not in visited:
                    visited.add(url)
                    frontier.append(url)