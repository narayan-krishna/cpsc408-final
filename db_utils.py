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
    def add_class(self, class_name, topic_list):
        sql_insert = "INSERT INTO Class (className) VALUES (%s);"
        vals = class_name
        topics_that_exist = []

        for topics in topic_list: 
            sql_select = "SELECT topicID FROM Topic WHERE TopicName = "+topics
            mycursor.execute(sql_select)
            results = mycursor.fetchall()
            for x in results: 
                print(x)
            for x in results: 
                topics_that_exist.append(x)
            #Here we need to check that the topics exist before we add them to the ClassTopics table. 
            mycursor.execute(sql_insert,vals)
            mydb.commit()
            print(mycursor.rowcount,"was inserted.")

            
        mycursor.execute(sql_insert,vals)
        classIDQuery = "SELECT classID FROM Class WHERE className = "+class_name
        mycursor.execute(classIDQuery)
        classID = mycursor.fetchall()
        for topics in topics_that_exist:
            sql_insert = "INSERT INTO ClassTopic (classID,topicID) VALUES (%s,%s)"
            vals = (classID,topics)
            mycursor.execute(sql_insert,vals)
            

        


    #TODO: implement add topic
    def add_topic(self, topic_name: str):
        sql_insert = "INSERT INTO Topic VALUES (%s);"
        vals = topic_name
        mycursor.execute(sql_insert,vals)
        mydb.commit()
        print(mycursor.rowcount,"was inserted.")

    
    #def set_up_user(self,)

        
        

    # close connection
    def destructor(self):
        # self.db.close()
        return

