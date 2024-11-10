# get the DB
import sqlite3

def DB (query,data):
    connection = sqlite3.connect('BrickByBalance.db')
    cursor = connection.cursor()
    cursor.execute(query, (data))
    data = cursor.fetchall()
    connection.close()
    return data