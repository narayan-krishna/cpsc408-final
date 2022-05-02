# db_utils.py
import mysql.connector
mydb = mysql.connector.connect(host="localhost",
user="root",
password="Sentry8949254816", # y'all pls don't hack meeeee
auth_plugin='mysql_native_password',
database="RideShare")

mycursor = mydb.cursor()


class db_utils():

    def __init__(self): # constructor with connection path to db
        print("")
        # self.db = mysql.connector.connect(host="",
        #                                user="",
        #                                password="",
        #                                auth_plugin='',
        #                                database="")
        # self.cursor = self.db.cursor()
        # print("connection made..")

    # TODO: implement add class
    def add_class(self, class_name):
        sql = "INSERT INTO Class VALUES (%s);"
        vals = class_name
        mycursor.execute(sql,vals)
        mydb.commit()
        print(mycursor.rowcount,"was inserted.")


    #TODO: implement add topic
    def add_topic(self, topic_name: str):
        return    

    # close connection
    def destructor(self):
        # self.db.close()
        return

