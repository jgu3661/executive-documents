# executive-documents

[Last updated August 3rd, 2021]
[Copyright © 2021 jgu3661]

## Description 

This code was written as part of research for [Professor Jon Rogowski](https://voices.uchicago.edu/jrogowski/)'s project on Unilateral Action and the Presidency. The aim is to better understand variation in how Presidents have leveraged the powers of the Executive Office over time. Part of this involves putting together a database of Presidential documents and manually inputting certain qualitative characteristics for each. We access these documents using Harvard's access to ProQuest Congressional. 

However, over the first few months of the project, more than half of our time was spent inputting identifying information about the documents that was already available in Proquest Congressional and required no subjective coding - title, date, permalink, etc. This code automates the gathering of these characteristics, scraping from our 76,000+ search results in ProQuest Congressional and outputting the relevant characteristics as CSVs separated by year from 1789 to 2021. 

## Setup and Usage

This program requires a HarvardKey login to access Proquest Congressional. After downloading the repo, create a `.env` file in the main directory and set your `HARVARDKEY_USERNAME`, `HARVARDKEY_PASSWORD`, and `WEBDRIVER_PATH` (the path to the executable you downloaded above.)

This program makes use of Selenium WebDriver, which requires an [executable](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/) specific to the browser in use. The appropriate download for Firefox, the browser this program uses, can be found [here](https://github.com/mozilla/geckodriver/releases). You can also use other browsers by installing the [appropriate executable](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/#quick-reference) and updating the lines 11 and 29 in `main.py`.

To use, run `python3 main.py` in the command line. The program will ask for a start and end year to scrape through; the earliest possible start year is 1789 and the latest possible end year is 2021. After inputting this information, depending on your internet connection, you will receive a Duo Mobile push notification within 20 seconds; approve it and the program will run by itself from there. 


