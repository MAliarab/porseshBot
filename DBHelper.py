

import datetime
import mysql.connector



DB_CONFIG = {
        'user':'mahmood',
        'database':'porseshBot',
        'passwd':'',
        'host':'127.0.0.1',
        'charset':'utf8'

}

def connection():

    cnx = mysql.connector.connect(user=DB_CONFIG['user'], database=DB_CONFIG['database'],host=DB_CONFIG['host'],charset=DB_CONFIG['charset'])
    # cnx.charset('utf-8')
    return  cnx


def setup_cursor(cnx):
    dbc = cnx.cursor()
    dbc.execute('SET NAMES utf8;')
    dbc.execute('SET CHARACTER SET utf8;')
    dbc.execute('SET character_set_connection=utf8;')
    return dbc


    # def Insert(self, cursor,table_name , Parametrs):

def executeQuery(query, cursor):

    cursor.execute(query)

def closeConnection(cursor,cnx):

    cursor.close()
    cnx.close()



def test(cursor,cnx):

    query1 = ("SELECT * FROM users")

    # cursor.execute(query1)
    #
    # for(name) in cursor:
    #
    #     print(type(name))
    #     print("{} was hired".format(
    #     name[1]))

    data_user = ('hassan', 20, "Engineering", 'M')

    #
    # query = ("INSERT INTO users "
    #          "(id,name, age, field, sex) "
    #          "VALUES (%s,%s, %s,%s, %s)")

    # query = "INSERT INTO users(name,age, field, sex) " \
    #         "VALUES(%s,%s,%s,%s)"
    #
    # cursor.execute(query,data_user)
    # cnx.commit()

    # cursor.execute(query1)
    # cnx.commit()
    #
    # for(name) in cursor:
    #
    #     print(type(name))
    #     print("{} was hired".format(
    #     name[1]))



cnx = connection()
cursor = setup_cursor(cnx)
test(cursor,cnx)

