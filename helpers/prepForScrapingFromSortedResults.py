# Once results are sorted, prepare to scrape them

def prepForScrapingFromSortedResults(driver):
    
    # Get number of results
    resultsSpan = driver.find_element_by_id('resultCountText')
    resultsTitle = resultsSpan.find_element_by_css_selector('h2.resultCount')
    resultsText = resultsTitle.get_attribute('innerHTML')
    resultsCount = int(resultsText.split()[0].replace(',',''))

    # Access first result
    firstResult = driver.find_element_by_class_name('itemPagingDiv')
    firstResultLink = firstResult.find_element_by_css_selector('a.itemTitle')
    firstResultLink.click()

    return driver, resultsCount