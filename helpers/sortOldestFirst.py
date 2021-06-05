# Sort results by date, with oldest documents appearing first

from . import constants
import time 

def sortOldestFirst(driver):

    # Sort search results chronologically
    sortDropdownButton = driver.find_element_by_id('sortSelectBtnGroup')
    sortDropdownButton.click()
    sortDateButton = sortDropdownButton.find_element_by_css_selector('a[data-sort="DATEOLD"]')
    sortDateButton.click()
    time.sleep(constants.shortTimeout) # Wait for results to sort

    return driver

