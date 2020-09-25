import mysql.connector
from mysql.connector import connect, errorcode, Error


def ConnectMySql():
    try:
        my_db = mysql.connector.connect(
            host="localhost", user="root", password="password", database="mydatabase",
        )
        return my_db
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return False
        else:
            print(err)
            return False
