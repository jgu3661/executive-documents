# Access URL protected with HarvardKey two-factor authentication

from . import constants
import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Access HarvardKey username and password, stored in the .env file
import os 
from dotenv import load_dotenv   
load_dotenv()                   
username = os.environ.get('HARVARDKEY_USERNAME')
password = os.environ.get('HARVARDKEY_PASSWORD')

def harvardKey2fa(driver, url):

    driver.get(url)

    wait = WebDriverWait(driver, constants.longTimeout)

    # Pass through redirect page
    redirectButton = wait.until(lambda d: 
        d.find_element_by_css_selector("input[value='here']"))
    redirectButton.click()

    # Log in with HarvardKey username and password
    loginForm = wait.until(lambda d:
        d.find_element_by_id("fm1")) # verify
    loginUsername = loginForm.find_element_by_id("username")
    loginUsername.send_keys(username)
    loginPassword = loginForm.find_element_by_id("password")
    loginPassword.send_keys(password)
    loginPassword.send_keys(Keys.RETURN)

    # Authenticate with 2FA
    duoIframe = wait.until(lambda d:
        d.find_element_by_id("duo_iframe"))
    driver.switch_to.frame(duoIframe)
    time.sleep(constants.shortTimeout) # Clicking instantly causes Duo Mobile to fail the authentication
    duoPushButton = wait.until(lambda d:
        d.find_element_by_css_selector('button.positive.auth-button'))
    driver.execute_script("arguments[0].click();", duoPushButton)
    driver.switch_to.default_content()
    
    return driver
