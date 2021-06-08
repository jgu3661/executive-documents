# Define constants

# Set default timeouts
shortTimeout = 5
medTimeout = 20
longTimeout = 60

# Clean date data
monthMapping = {
    'Jan': 1,
    'January': 1,
    'Feb': 2,
    'February': 2,
    'Mar': 3, 
    'March': 3,
    'Ap': 4, # One typo in 2016-PR-9431 :(
    'Apr': 4,
    'April': 4,
    'May' : 5,
    'June': 6,
    'July': 7,
    'Aug': 8,
    'August': 8,
    'Sept': 9,
    'September': 9,
    'Oct': 10,
    'October': 10,
    'Nov': 11,
    'November': 11,
    'Dec': 12,
    'December': 12,
}

# Define CSV header
fieldnames = ['accession', 'year', 'month', 'day', 'title', 'permalink', 'notes']