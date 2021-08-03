# Ask user for range of years to scrape

def getInput():
    while True:
        try:
            startYear = int(input('Enter start year (earliest documents are from 1789): ').strip())
            break
        except ValueError:
            print("That's not a number!")

    while True:
        try:
            endYear = int(input('Enter end year: ').strip())
            break
        except ValueError:
            print("That's not a number!")

    return startYear, endYear