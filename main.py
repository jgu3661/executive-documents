# Construct database of executive documents using Proquest Congressional

# Import helpers
from helpers.getInput import getInput
from helpers.harvardKey2fa import harvardKey2fa
from helpers.presidentialSearchAndFilter import presidentialSearchAndFilter
from helpers.sortOldestFirst import sortOldestFirst
from helpers.scrapeYears import scrapeYears

# Import web driver
from selenium import webdriver



def main():

    # Get years from user
    startYear, endYear = getInput()

    # Start driver session
    driver = webdriver.Firefox()

    # Go to Proquest Congressional
    proquestCongressionalUrl = 'http://nrs.harvard.edu/urn-3:hul.eresource:conguniv'
    driver = harvardKey2fa(driver, proquestCongressionalUrl)

    # Enter search, then filter results accordingly
    driver = presidentialSearchAndFilter(driver)

    # Sort chronologically
    driver = sortOldestFirst(driver)

    # Scrape through desired years
    driver = scrapeYears(driver, startYear, endYear)

    # Close driver session
    driver.close()



main()