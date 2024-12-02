from bs4 import BeautifulSoup
from database import *

def parser(targets):

    # find the target documents in the pages collection
    targets = pages_collection.find({'isTarget': True})

    for target in targets:
        target_content = target['content']
        bs = BeautifulSoup(target_content, 'html.parser')
        
        # fac-staff and accolades are the search areas. need to extract just text

        fac_staff = bs.find('div', {'class': 'fac-staff'}).find_all('div', {'class': 'col'})
        fac_staff_list = [' '.join(staff.get_text(strip=True).split()) for staff in fac_staff]

        # might have to come back to this so that only text is extracted
        accolades = bs.find('div', {'class': 'accolades'})
        accolades_list = [' '.join(accolade.get_text(strip=True).split()) for accolade in accolades]
        
        fac_staff_str = ' '.join(fac_staff_list)
        accolade_str = ' '.join(accolades_list)

        combined = ''
        combined += fac_staff_str
        combined += accolade_str

        # insert into mongodb
        search_content_collection.update_one(
            { '_id': target['_id'] },
            { '$set': { 'content': combined } },
            upsert = True
        )