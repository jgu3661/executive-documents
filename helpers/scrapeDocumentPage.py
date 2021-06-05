# Scrape relevant info from a Proquest Congressional document page

from . import constants
import re
from selenium.webdriver.support.ui import WebDriverWait

# Used for data cleaning
monthMapping = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3, 
    'Apr': 4,
    'May' : 5,
    'June': 6,
    'July': 7,
    'Aug': 8,
    'Sept': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}

def scrapeDocumentPage(driver, writer):
    
    contents = WebDriverWait(driver, constants.longTimeout).until(lambda d: 
        d.find_element_by_class_name('docsContentRow'))
    contentRows = contents.find_elements_by_css_selector('div.docSegRow')
    relevantInfoRows = contentRows[:3]
    relevantInfoRows.append(contentRows[-1])
    relevantInfoElements = [e.find_element_by_class_name('segColR') for e in relevantInfoRows]
    relevantInfo = [e.get_attribute('innerHTML') for e in relevantInfoElements]

    row = {}
    row["accession"] = re.sub('<.*?em.*?>', '', relevantInfo[0]).strip()

    date = re.sub('<.*?em.*?>', '', relevantInfo[2]).replace('.','')
    dateParts = date.split()

    if len(dateParts) == 3:
        row["year"] = int(dateParts[2])
        row["month"] = monthMapping[dateParts[0]]
        row["day"] = int(dateParts[1].replace(',',''))
    elif len(dateParts) == 1:
        row["year"] = int(dateParts[0])
    else:
        row["notes"] = f'Date field was {date}'

    row["title"] = re.sub('<.*?span.*?>', '', re.sub('<.*?em.*?>', '', relevantInfo[1])).strip()
    row["permalink"] = re.sub('<.*?em.*?>', '', relevantInfo[3]) 

    writer.writerow(row)
    
    return (driver, writer)
