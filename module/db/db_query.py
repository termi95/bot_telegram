#!/usr/bin/python3
from termcolor import colored
from configparser import ConfigParser
import psycopg2
import datetime

config = ConfigParser()
config.read('/home/termi/bot_telegram/config.ini')

def __connect():
     #""" Connect to the PostgreSQL database server """
    try:
        # connect to the PostgreSQL server               
        return psycopg2.connect(
            host = config.get('db', 'host'),
            database = config.get('db', 'database'),
            user = config.get('db', 'user'),
            password = config.get('db', 'password')
            )       
    except (Exception, psycopg2.DatabaseError) as error:
        print("error: " + str(error))

def __closeConnect(cursor):
    cursor.close()

def insertVideo(listOfVideo):
    conn = __connect()    
    # create a cursor
    cursor = conn.cursor() 
    # Get date when movie was added
    date = datetime.date.today()
    # Query to add video
    sql = "INSERT INTO video(url, date) VALUES(%s, %s)" 
    
    for url in listOfVideo:
        try:
            # execute a statement
            print('try insert data')
            cursor.execute(sql, (url, date))
            # commit the changes to the database
            conn.commit()
            print(colored('insert data', config.get('termColor','OK')))
        except (Exception, psycopg2.DatabaseError) as error:
            print(colored("error: " + str(error) + 'trying to do rollback', config.get('termColor','FAIL')))
            conn.rollback()
    __closeConnect(cursor)

def getVideo():
    listOfVideo = []
    conn = __connect()    
    # create a cursor
    cursor = conn.cursor()
    # Query to add video
    sql = "SELECT url FROM video"  
    try:
        # execute a statement
        cursor.execute(sql)
        # get video from database
        videoFromDb = cursor.fetchall() 
        for video in videoFromDb:
            listOfVideo.append(video[0])
    except (Exception, psycopg2.DatabaseError) as error:
        print(colored("error: " + str(error), config.get('termColor','FAIL')))
    __closeConnect(cursor)
    return listOfVideo

def getMemeHistoryForUser(userId):
    memeHistoryList = []
    conn = __connect()
    # create a cursosr
    cursor = conn.cursor()
    # Query to get user history
    sql = "SELECT meme FROM meme_history WHERE user_id = %s;"
    try:
        # Execute a statement
        cursor.execute(sql, [userId])
        # Get history
        historyFromDb = cursor.fetchall()
        # create list to easier check
        for meme in historyFromDb:
            memeHistoryList.append(meme[0])
    except (Exception, psycopg2.DatabaseError) as error:
            print(colored("error: " + str(error), config.get('termColor', 'FAIL')))
    __closeConnect(cursor)
    return memeHistoryList

def updateHistory(userId, meme, content_type):
    conn = __connect()
    # create a cursor
    cursor = conn.cursor()
    # Get date when movie was added
    date = datetime.date.today()
    # Query to add video
    sql = "INSERT INTO meme_history(user_id, meme, date, content_type) VALUES(%s, %s, %s, %s)"
    try:
        # execute a statement
        cursor.execute(sql, (userId, meme, date, content_type))
        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(colored("error: " + str(error) + 'trying to do rollback', config.get('termColor','FAIL')))
        conn.rollback()
    __closeConnect(cursor)

def getViewedMemeForUser(userId, content_type = '/photo'):    
    conn = __connect()
    # create a cursor
    cursor = conn.cursor()
    # Query to add video
    sql = "SELECT COUNT(meme) FROM meme_history where user_id=%s AND content_type=%s"
    try:
        # execute a statement
        cursor.execute(sql, (userId, content_type))
        # commit the changes to the database
        return cursor.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(colored("error: " + str(error) + 'trying to do rollback', config.get('termColor','FAIL')))
        conn.rollback()
    __closeConnect(cursor)

def sign(user_id, first_name, last_name = None, username = None) -> None:
    conn = __connect()
    # create a cursor
    cursor = conn.cursor()
    # Query to add video
    sql = 'INSERT INTO "user"(user_id, first_name, last_name, username) VALUES(%s, %s, %s, %s)'
    try:
        # execute a statement
        cursor.execute(sql, (user_id, first_name, last_name, username))
        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(colored("error: " + str(error) + 'trying to do rollback', config.get('termColor','FAIL')))
        conn.rollback()
        try:
            # execute a statement
            sql = 'UPDATE "user" SET first_name = \'{}\', last_name = \'{}\', username = \'{}\' WHERE user_id = \'{}\';'.format(first_name,last_name,username,user_id)
            cursor.execute(sql, (user_id, first_name, last_name, username))
            # commit the changes to the database
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(colored("error: " + str(error) + 'trying to do rollback', config.get('termColor','FAIL')))
            conn.rollback()
        
    __closeConnect(cursor)

def updateUser(user_id, first_name, last_name = None, username = None) -> None:
    conn = __connect()
    # create a cursor
    cursor = conn.cursor()
    try:
        # execute a statement
        sql = 'UPDATE "user" SET first_name = \'{}\', last_name = \'{}\', username = \'{}\' WHERE user_id = \'{}\';'.format(first_name,last_name,username,user_id)
        cursor.execute(sql, (user_id, first_name, last_name, username))
        # commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(colored("error: " + str(error) + 'trying to do rollback', config.get('termColor','FAIL')))
        conn.rollback()
        
    __closeConnect(cursor)
    
def checkUserExist(user_id) -> int:
    conn = __connect()
    # create a cursor
    cursor = conn.cursor()
    # execute a statement
    sql = 'SELECT "user".user_id FROM "user" WHERE user_id = {};'.format(user_id)
    try:
        # execute a statement
        cursor.execute(sql)
        # commit the changes to the database
        return len(cursor.fetchall())
    except (Exception, psycopg2.DatabaseError) as error:
        print(colored("error: " + str(error) + 'trying to do rollback', config.get('termColor','FAIL')))
        conn.rollback()
        
    __closeConnect(cursor)

def getMemeRank():        
    conn = __connect()
    # create a cursor
    cursor = conn.cursor()
    # Query to add video
    sql =   """
                SELECT "user".first_name, "user".last_name, "user".username, COUNT(meme) AS zobaczone_memy
                FROM meme_history
                INNER JOIN "user" ON "user".user_id=meme_history.user_id
                WHERE content_type = '/photo'
                GROUP  BY "user".user_id
                ORDER BY COUNT(meme) DESC
                LIMIT 5;
            """
    try:
        # execute a statement
        cursor.execute(sql)
        # commit the changes to the database
        return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(colored("error: " + str(error) + 'trying to do rollback', config.get('termColor','FAIL')))
        conn.rollback()
    __closeConnect(cursor)