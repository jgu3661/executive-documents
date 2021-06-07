# Scrape relevant info from a Proquest Congressional document page

import re
from .constants import monthMapping

def scrapeDocumentPage(soup):
    
    contents = soup.find('div', class_='docsContentRow')
    contentRows = contents.find_all('div', class_='docSegRow')
    relevantInfoRows = contentRows[:3]
    relevantInfoRows.append(contentRows[-1])
    relevantInfoElements = [e.find('div', class_='segColR') for e in relevantInfoRows]
    relevantInfo = [e.text for e in relevantInfoElements]
    relevantInfoClean = [re.sub('<.*?em.*?>', '', e).strip() for e in relevantInfo]

    try: 
        row = {}
        row["accession"] = relevantInfoClean[0]

        date = relevantInfoClean[2].replace('.','').replace(',', '')
        dateParts = date.split()

        if len(dateParts) == 3:
            row["year"] = int(dateParts[2])
            row["month"] = monthMapping[dateParts[0]]
            row["day"] = int(dateParts[1])
        elif len(dateParts) == 1:
            row["year"] = int(dateParts[0])
        else:
            row["notes"] = f'Date field was {date}'
        

        row["title"] = re.sub('<.*?span.*?>', '', relevantInfoClean[1]).strip()
        row["permalink"] = relevantInfoClean[3]
    
    except ValueError:
        row["notes"] = "This entry was missing some info; please check manually."
    
    return row
