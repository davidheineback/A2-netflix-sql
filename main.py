import pandas as pd
import numpy as np
import mysql.connector as my_sql
from mysql.connector import errorcode

# Read csv files
shows = pd.read_csv('./shows.csv', delimiter=',')
streaming_service = pd.read_csv('./streaming_service.csv', delimiter=',')
streams_on = pd.read_csv('./streams_on.csv', delimiter=',')

shows = shows.replace(np.nan, None)
shows['imdb'] = shows['imdb'].map(lambda x: x.replace('/10', '') if x is not None else x)
shows['rotten_tomatoes'] = shows['rotten_tomatoes'].map(lambda x: x.replace('/100', '') if x is not None else x)
streaming_service = streaming_service.replace(np.nan, None)
df = pd.DataFrame(streams_on)
df = df.astype({"movie_ID":"str","streaming_ID":"str"})
streams_on = df.replace(np.nan, None) 

# Create tuples by row
shows_tuples = [tuple(row) for row in shows.values]
streaming_service_tuples = [tuple(row) for row in streaming_service.values]
streams_on_tuples = [tuple(row) for row in streams_on.values]

# create a sql connection
connection = my_sql.connect(
        host='localhost',
        port='8889',
        user='root',
        password='root'
        )

#DB Name
DB_NAME = 'streaming_data'

cursor = connection.cursor()

# Method to create the database
def create_database(cursor, DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except my_sql.Error as err:
        print("Faild to create database {}".format(err))
        exit(1)
        
# Create the table for shows
def create_table_shows(cursor):
    create_shows = (
    "CREATE TABLE `shows`("
    " `ID` varchar(255) NOT NULL,"
    " `title` varchar(255) NULL,"
    " `year` varchar(255) NULL,"
    " `age` varchar(255) NULL,"
    " `imdb` float(3) NULL,"
    " `rotten_tomatoes` int(3) NULL,"
    " PRIMARY KEY (ID))")
    try:
        print("Creating table shows: ")
        cursor.execute(create_shows)
    except my_sql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
        
# add shows to the db table
def add_shows_to_db(cursor):
    for show in shows_tuples:
        sql = ("INSERT INTO shows "
               "(ID, title, "
               "year, age, "
               "imdb, rotten_tomatoes) "
               "VALUES(%s, %s, %s, %s, %s, %s)")
        try:
            cursor.execute(sql, show)
        except:
            pass
          
# Create the table for streaming services
def create_table_streaming_service(cursor):
    create_service = (
    "CREATE TABLE `streaming_services`("
    " `ID` varchar(255) NOT NULL,"
    " `streaming_service` varchar(255) NULL,"
    " PRIMARY KEY (ID))")
    try:
        print("Creating table streaming_services: ")
        cursor.execute(create_service)
    except my_sql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
        
# add streaming to the db table
def add_services_to_db(cursor):
    for service in streaming_service_tuples:
        sql = ("INSERT INTO streaming_services "
               "(ID, streaming_service) "
               "VALUES(%s, %s)")
        try:
            cursor.execute(sql, service)
        except:
            pass
          
# Create the table for streaming services
def create_table_streams_on(cursor):
    create_streams = (
    "CREATE TABLE `streams_on`("
    " `movie_ID` varchar(255) NOT NULL,"
    " `streaming_ID` varchar(255) NOT NULL,"
    " FOREIGN KEY (movie_ID) REFERENCES shows(ID), "
    " FOREIGN KEY (streaming_ID) REFERENCES streaming_services(ID))")
    try:
        print("Creating table streams_on: ")
        cursor.execute(create_streams)
    except my_sql.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
        
# add streaming to the db table
def add_streams_to_db(cursor):
    for stream in streams_on_tuples:
        sql = ("INSERT INTO streams_on "
               "(movie_ID, streaming_ID) "
               "VALUES(%s, %s)")
        try:
            cursor.execute(sql, stream)
        except Exception as err:
            print(err)
          
          
# run the sequence and create the DB if not existing
try:
    cursor.execute("USE {}".format(DB_NAME))
except my_sql.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database {} does not exist".format(DB_NAME))
        create_database(cursor, DB_NAME)
        print("Database {} created succesfully.".format(DB_NAME))
        connection.database = DB_NAME
        create_table_shows(cursor)
        add_shows_to_db(cursor)
        create_table_streaming_service(cursor)
        add_services_to_db(cursor)
        connection.commit()
        create_table_streams_on(cursor)
        add_streams_to_db(cursor)
        connection.commit()
    else:
        print(err)

cursor.close()
connection.close()