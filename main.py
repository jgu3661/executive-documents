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
    driver = scrapeYears(driver, startYear, endYear, advancedSearchUrl)

    # Close the driver
    driver.close()



main()