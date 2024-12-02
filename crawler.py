import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
from database import *

# initialize frontier
frontier = deque()
frontier.append('https://www.cpp.edu/engineering/ce/index.shtml')

# initialize set for visited links
visited = set()

NUMBER_TARGETS = 10

# define re for easier access to expression

relative_url = r'^(?!https?:\/\/www.)'
cpp_base =  "https://www.cpp.edu/"

while frontier:
    # get the next URL from the queue
    url = frontier.popleft()
    # html = urlopen(url)
    try:
        html = urlopen(url)
    except Exception as e:
        print(e)
    
    data = html.read()

    bs = BeautifulSoup(data, 'html.parser')

    # initialize counter for number of targets
    targets_found = 0

    # check if target is found (header is found)
    target = bs.find('div', {'class': 'fac-info'})
    if target:
        pages.insert_one({'url': url, 'html': data.decode('utf-8'), 'isTarget': True})
        targets_found += 1

        # check if number_targets is reached
        if targets_found == NUMBER_TARGETS:
            frontier.clear()
            break
    else:
        pages.insert_one({'url': url, 'html': data.decode('utf-8')})
        linked_urls = []

        a_tag = bs.find_all('a', href=True)

        for tag in a_tag:
            url = tag['href'].strip()

            if url.endswith('/'):
                url = url[:-1]
            
            if re.match(relative_url, url):
                # clean / in beginning of relative url
                if url.startswith('/'):
                    url = url[1:]
                
                if url.startswith('~'):
                    url = url[1:]
                url = cpp_base + url
            
            if re.match(cpp_base, url):
                # append url to visited array
                if url not in visited:
                    linked_urls.append(url)

        for url in linked_urls:
            if url not in visited:
                visited.add(url)
                frontier.append(url)
