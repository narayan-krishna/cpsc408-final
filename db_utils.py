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


    def add_class(self, class_name):
        sql_insert = "INSERT INTO Class (className) VALUES (%s);"
        vals = class_name
        mycursor.execute(sql_insert,vals)
        mydb.commit()
        print(mycursor.rowcount,"was inserted.")
            

    def add_topic(self, topic_name): 
        sql_insert = "INSERT INTO Topic (topicName) VALUES (%s);"
        vals = topic_name
        mycursor.execute(sql_insert,vals)
        mydb.commit()
        print(mycursor.rowcount,"was inserted.")
        
    def add_class_topic(self, class_name: str, topic_names):
        for name in topic_names:
            sql_select = "SELECT topicID FROM Topic WHERE topicName = "+name+";"
            mycursor.execute(sql_select)
            topicID = mycursor.fetchall()
            if (topicID != ""): #ie the topic does not exist
                self.add_topic(name)
                sql_select = "SELECT topicID FROM Topic WHERE topicName = "+name+";"
                mycursor.execute(sql_select)
                topicID = mycursor.fetchall()

            sql_insert = "INSERT INTO ClassTopic (classID,topicID) VALUES (%s,%s);"
            classIDSelect = "SELECT classID FROM Class WHERE className ="+class_name+";"
            mycursor.execute(classIDSelect)
            classID = mycursor.fetchall()
            vals = (classID,topicID)
            mycursor.execute(sql_insert,vals)

    
    #def set_up_user(self,)

   

    # close connection
    def destructor(self):
        # self.db.close()
        return

