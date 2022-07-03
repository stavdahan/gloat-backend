from random import random
import mysql.connector
from mysql.connector import errorcode
from database import cursor, db
from faker import Faker
import random
fake = Faker()

DB_NAME = 'matcherdb'

TABLES = {}

TABLES['candidates'] = (
    "CREATE TABLE `candidates` ("
    " `id` int(11) NOT NULL AUTO_INCREMENT,"
    " `name` varchar(50) NOT NULL,"
    " `title` varchar(50) NOT NULL,"
    " `skills` varchar(100) NOT NULL,"
    " PRIMARY KEY (`id`)"
    ") "
)

titles = ('Software engineer', 'Backend Developer','Frontend Developer', 'Software Developer')
skills = ('C', 'C++', 'JS', 'Python', 'Java', 'C#', 'React', 'Django',
          'NodeJS', '.net Core', 'Flask', 'Fastapi', 'Angular', 'Vue', 'React Native')

def create_database():
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8' "
    )
    print(f"Database {DB_NAME} created!")

def create_tables():
    cursor.execute(f"USE {DB_NAME}")

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table ({table_name})", end="")
            cursor.execute(table_description)
            fill_mock_data()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Already Exists')
            else:
                print(err.msg)

def fill_mock_data():
    for number in range(500): 
        personal_skills = set()
        for random_number in range(random.randint(1, 7)):
            personal_skills.add(random.choice(skills))
        #person = Candidate(name=fake.name(), title=random.choice(titles), skills= ', '.join(personal_skills))
        person = {
            'name': f"{fake.name()}",
            'title': f"{random.choice(titles)}",
            'skills': personal_skills,
        }
        cursor.execute(f"INSERT INTO candidates (name, title, skills) VALUES('{person['name'].lower()}', '{person['title'].lower()}', '{', '.join(person['skills']).lower()}')")
        db.commit()



create_database()
create_tables()


