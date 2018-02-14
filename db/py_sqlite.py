import sqlite3

def db_create(mydb,c_query):
    connection = sqlite3.connect(mydb)
    with connection:
        cursor = connection.cursor()
        #Below line for debugging purpose
        #c_query = "create table if not exists build_details(CVE string, package string,ptime string)"
        cursor.execute(c_query)
        connection.commit()

    if connection:
       connection.close()

def db_insert(mydb,i_query):
    connection = sqlite3.connect(mydb)
    with connection:
        cursor = connection.cursor()
        print i_query
        cursor.execute(i_query)
        connection.commit()

    if connection:
       connection.close()

def db_select1(mydb,s_query):
    connection = sqlite3.connect(mydb)
    with connection:
        cursor = connection.cursor()
        print s_query
        cursor.execute(s_query)
        r = cursor.fetchone()[0]
        connection.commit()
        return r

    if connection:
       connection.close()
