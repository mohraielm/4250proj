from bs4 import BeautifulSoup
from database import *

# find the target documents in the pages collection

targets = pages.find({'isTarget': True})

for target in targets:
    target_content = target['html']
    bs = BeautifulSoup(target_content, 'html.parser')
    
    # fac-staff and accolades are the search areas. need to extract just text

    fac_staff = bs.find('div', {'class': 'fac-staff'}).find_all('div', {'class': 'col'})
    fac_staff_text = [' '.join(staff.get_text(strip=True).split()) for staff in fac_staff]

    # might have to come back to this so that only text is extracted
    accolades = bs.find('div', {'class': 'accolades'})
    accolades_text = [' '.join(accolade.get_text(strip=True).split()) for accolade in accolades]

    combined_list = []
    combined_list = fac_staff_text + accolades_text
    cleaned_list = [item for item in combined_list if item not in (None, '')]
    print(cleaned_list)

    # insert into mongodb
    search_content.insert_one({'text': combined_list})

