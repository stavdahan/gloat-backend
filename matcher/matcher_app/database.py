import mysql.connector

# change the user and the password
config = {
    'user': '',
    'password': '',
    'host': 'localhost',
    'database': 'matcherdb',
}

db = mysql.connector.connect(**config)
cursor = db.cursor()