# Once results are sorted, prepare to scrape them

from . import constants
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def openSkipTo(driver, skipTo):

    wait = WebDriverWait(driver, constants.longTimeout)

    # Click next to the correct results page
    nextPageClicks = skipTo // 20
    resultNumberOnPage = skipTo % 20

    for i in range(nextPageClicks):
        nextButton = wait.until(lambda d:
            d.find_element_by_id('btnNext'))
        nextButton.click()
        wait.until(EC.staleness_of(nextButton))

    # Access first result to be scraped
    if resultNumberOnPage == 19:
        firstResult = driver.find_element_by_class_name('itemPagingLastDiv')
    else:
        firstResult = driver.find_elements_by_class_name('itemPagingDiv')[resultNumberOnPage]
    firstResultLink = firstResult.find_element_by_css_selector('a.itemTitle')
    firstResultLink.click()

    # Make sure the old page is gone before continuing
    wait.until(EC.staleness_of(firstResult))

    return driver