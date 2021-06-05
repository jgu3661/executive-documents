# Enter search on Proquest Congressional's Advanced Search page, 
#   then filter results accordingly. 

from . import constants
import time 
from selenium.webdriver.support.ui import WebDriverWait

def presidentialSearchAndFilter(driver):

    # Shorthand for loading waiting
    wait = WebDriverWait(driver, constants.longTimeout)

    # Select categories of documents to use
    allCategoriesButton = wait.until(lambda d:
        d.find_element_by_id("selectAll_Adv"))
    allCategoriesButton.click()
    presidentialMaterialButton = driver.find_element_by_id("eopr")
    presidentialMaterialButton.click()

    # Enter search terms
    searchBar = driver.find_element_by_id("searchText")
    searchBar.send_keys("president")
    searchButton = driver.find_element_by_css_selector('a#submitHidden_1>span')
    searchButton.click()

    # Filter search results
    docTypeOptionsButton = wait.until(lambda d:
        d.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[5]/div[2]/div/div/div[2]/div/div/dl/div/div[3]/div[2]/div[2]/div[2]/span'))
    docTypeOptionsButton.click()
    docTypePlusButton = wait.until(lambda d:
        d.find_element_by_xpath('/html/body/div[18]/div/div/div[2]/div/div/div[2]/div/div[1]/div[3]/span[1]'))
    driver.execute_script("arguments[0].click();", docTypePlusButton)

    excludeButtons = [
        'exclude_Executive Orders and Presidential Proclamations_Presidential Pardons_2',
        'exclude_Executive Orders and Presidential Proclamations_Presidential Signing Statements_7',
        'exclude_Executive Orders and Presidential Proclamations_Administrative Policy Statements_8',
        'exclude_Executive Orders and Presidential Proclamations_Nominations and Appointments_9'
    ]

    for excludeString in excludeButtons:
        wait.until(lambda d: 
            d.find_element_by_css_selector(f"label[for='{excludeString}']")).click()

    applyFiltersButton = driver.find_element_by_xpath('/html/body/div[18]/div/div/div[3]/div/div[2]/button')
    applyFiltersButton.click()
    time.sleep(constants.shortTimeout) # Wait for filters menu to fade out

    return driver