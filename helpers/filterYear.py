# Filter results by a given year

from . import constants
import time
from selenium.webdriver.support.ui import WebDriverWait

def filterYear(driver, year):

    # Type in start and end years
    startField = WebDriverWait(driver, constants.longTimeout).until(lambda d: 
        d.find_element_by_id('txtDate1'))
    startField.clear()
    startField.click()
    startField.send_keys(f'01/01/{year}')
    endField = driver.find_element_by_id('txtDate2')
    endField.clear()
    endField.click()
    endField.send_keys(f'12/31/{year}')

    # Update search filters
    updateHolder = driver.find_element_by_class_name('divUpdateHolder')
    updateButton = updateHolder.find_element_by_tag_name('button')
    updateButton.click()

    # Wait for update to occur
    time.sleep(constants.shortTimeout)

    return driver