import psycopg2 as pcg
from decouple import config

DATABASE_URL = config('DATABASE_URL')

def create_table():
    with pcg.connect(DATABASE_URL, sslmode='require') as conn: # connect to the database
        with conn.cursor() as cur: # create a cursor object
            try:
                cur.execute('CREATE TABLE last_news (topic varchar, last_new varchar);') # creating a table

                topics = config('topics').split(', ')

                for topic in topics:
                    cur.execute('INSERT INTO last_news (topic, last_new) VALUES (%s, %s);', (topic, 'None'))

                conn.commit() # committing the changes
            except pcg.errors.DuplicateTable:
                print('Table already exists')
            else:
                print('Table created successfully')

def insert_data(kwargs: dict):
    with pcg.connect(DATABASE_URL, sslmode='require') as conn: # connect to the database
        with conn.cursor() as cur: # create a cursor object
            for key, value in kwargs.items():
                cur.execute('''
                    UPDATE last_news
                    SET last_new = %s
                    WHERE topic = %s;
                ''',
                (value, key)) # inserting data
            conn.commit() # committing the changes

def query_data():
    with pcg.connect(DATABASE_URL, sslmode='require') as conn: # connect to the database
        with conn.cursor() as cur: # create a cursor object
            cur.execute(f'SELECT * FROM last_news;') # query data
            rows = cur.fetchall() # fetch data
            return rows

create_table()
topics = config('topics').split(', ')
insert_data({topics[0]: 'test a', topics[1]: 'test b', topics[2]: 'test c'})
print(query_data())