# Scrape the data from the given range of years

from . import constants
from .filterYear import filterYear
from .prepForScrapingFromSortedResults import prepForScrapingFromSortedResults
from .scrapeDocumentPage import scrapeDocumentPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from csv import DictWriter
from bs4 import BeautifulSoup

def scrapeYears(driver, start, end):

    wait = WebDriverWait(driver, constants.longTimeout)

    for year in range(start, end+1):

        try:

            # Scrape results into CSV file for this year
            with open(f'output/{year}.csv', 'w', newline='') as csvfile:

                # Filter by year
                driver = filterYear(driver, year)

                # Once results are sorted, prepare to scrape them
                driver, resultsCount = prepForScrapingFromSortedResults(driver)

                # Begin CSV file
                fieldnames = ['accession', 'year', 'month', 'day', 'title', 'permalink', 'notes']
                writer = DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # Iterate through results
                for i in range(resultsCount-1):

                    # Wait until page has finished loading, then switch to soup
                    wait.until(lambda d: 
                        d.find_element_by_class_name('docsContentRow'))
                    soup = BeautifulSoup(driver.page_source, 'lxml')

                    # Scrape relevant info to CSV
                    row = scrapeDocumentPage(soup)
                    writer.writerow(row)

                    # Move onto the next result
                    nextButton = driver.find_element_by_css_selector('span.uxf-icon.uxf-right-open-large')
                    nextButton.click()

                    # Make sure the old page is gone before continuing
                    wait.until(EC.staleness_of(nextButton))

                # Get last result
                wait.until(lambda d: 
                    d.find_element_by_class_name('docsContentRow'))
                soup = BeautifulSoup(driver.page_source, 'lxml')
                row = scrapeDocumentPage(soup)
                writer.writerow(row)

            # Navigate back to search results to update filtered year
            backToResultsButton = wait.until(lambda d: 
                d.find_element_by_link_text('Back to Results'))
            backToResultsButton.click()
            wait.until(EC.staleness_of(backToResultsButton))
            
        except TimeoutException:
            print("Oops! Looks like Proquest Congressional had an unexpected error.")
            print(f"We finished scraping through {year-1}; to continue, run the program again starting from {year}.")
            return driver
    
    return driver