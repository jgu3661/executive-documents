# Construct database of executive documents using Proquest Congressional

# Import helpers
import helpers.constants as constants
from helpers.getInput import getInput
from helpers.harvardKey2fa import harvardKey2fa
from helpers.scrapeYears import scrapeYears

# Import web driver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait

# Import web driver path
import os 
from dotenv import load_dotenv   
load_dotenv()                   
path = os.environ.get('WEBDRIVER_PATH')

def main():

    # Get years from user
    startYear, endYear = getInput()

    # Start driver session
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Firefox(options=options, executable_path=path)

    # Go to Proquest Congressional
    proquestCongressionalUrl = 'http://nrs.harvard.edu/urn-3:hul.eresource:conguniv'
    driver = harvardKey2fa(driver, proquestCongressionalUrl)
    WebDriverWait(driver, constants.longTimeout).until(lambda d:
        d.find_element_by_id("selectAll_Adv"))

    # Scrape through desired years
    advancedSearchUrl = driver.current_url
    driver, year, err = scrapeYears(driver, startYear, endYear, advancedSearchUrl)

    # Print error messages, if there are any
    if year != -1:
        print("Oops! Looks like Proquest Congressional had an unexpected error.")
        if year != startYear:
            print(f"We finished scraping through {year-1}; to continue, run the program again starting from {year}.")
        else:
            print("Please try again.")
            
    # Close the driver
    driver.close()



main()