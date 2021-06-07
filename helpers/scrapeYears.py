# Scrape the data from the given range of years

from . import constants
from .presidentialSearchAndFilter import presidentialSearchAndFilter
from .sortOldestFirst import sortOldestFirst
from .filterYear import filterYear
from .openSkipTo import openSkipTo
from .scrapeDocumentPage import scrapeDocumentPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from csv import DictWriter
from bs4 import BeautifulSoup

def scrapeYears(driver, start, end, advancedSearchUrl, skipTo=0):

    wait = WebDriverWait(driver, constants.longTimeout)

    # Reset to Advanced Search page
    driver.get(advancedSearchUrl)

    # Enter search, then filter results accordingly
    driver = presidentialSearchAndFilter(driver)

    # Sort chronologically
    driver = sortOldestFirst(driver)

    for year in range(start, end+1): 

        try:

            # Filter by year
            driver = filterYear(driver, year)

            # Scrape results into CSV file for this year
            if skipTo == 0:
                csvfile = open(f'output/{year}.csv', 'w', newline='')

                # Begin CSV file
                writer = DictWriter(csvfile, fieldnames=constants.fieldnames)
                writer.writeheader()
            
            else:
                csvfile = open(f'output/{year}.csv', 'a', newline='')
                writer = DictWriter(csvfile, fieldnames=constants.fieldnames)

            resultsText = driver.find_element_by_css_selector('h2.resultCount').get_attribute('innerHTML')
            resultsCount = int(resultsText.split()[0].replace(',',''))

            # Open the result from which to start
            driver = openSkipTo(driver, skipTo)

            # Iterate through results
            for i in range(resultsCount-skipTo):
                print(f'{year}, {skipTo+i}')
                # Wait until page has finished loading, then switch to soup
                wait.until(lambda d: 
                    d.find_element_by_class_name('docsContentRow'))
                soup = BeautifulSoup(driver.page_source, 'lxml')

                # Scrape relevant info to CSV
                row = scrapeDocumentPage(soup)
                writer.writerow(row)

                # Move onto the next result
                try:
                    nextButton = driver.find_element_by_css_selector('a[title="next document"]')
                except NoSuchElementException:
                    csvfile.close()
                    break
                nextButton.click()

                # Make sure the old page is gone before continuing
                wait.until(EC.staleness_of(nextButton))

            # Navigate back to search results to update filtered year
            backToResultsButton = wait.until(lambda d: 
                d.find_element_by_link_text('Back to Results'))
            backToResultsButton.click()
            wait.until(EC.staleness_of(backToResultsButton))
            if year == start:
                skipTo = 0
            
        except TimeoutException:
            
            csvfile.close()

            # Check if the page is a GIS System Error page
            try:
                driver.find_element_by_css_selector('h2[title="GIS System Error"]')

                # If it is, run scrapeYears again, skipping to the result we left off on
                return scrapeYears(driver, year, end, advancedSearchUrl, skipTo=i+skipTo)
            
            # If it's not, I have no idea what happened. 
            except NoSuchElementException as err:
                return driver, year, err
    
    return driver, -1, None