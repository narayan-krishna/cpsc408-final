# db_utils.py
import mysql.connector
import random

mydb = mysql.connector.connect(host="localhost",
user="root",
password="Sentry8949254816", # y'all pls don't hack meeeee
auth_plugin='mysql_native_password',
database="WizBot")

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


    def sql_injection_check(self,string): 
        if (str(string).find("DROP") != -1) or (str(string).find("SELECT") != -1) or (str(string).find("UPDATE") != -1) or (str(string).find("DELETE") != -1) or (str(string).find("INSERT") != -1): 
            print("Sorry, input was suspect and so was dropped for your security.")
            return False
        else: 
            return True


    def get_class_id(self,class_name): 
        classID_query = "SELECT classID FROM Class WHERE className = %s;"
        vals = (
            (class_name,)
        )
        mycursor.execute(classID_query,vals)
        mydb.commit()
        classID = mycursor.fetchall()
        return classID


    def add_class_member(self,classID,userID):
        class_member_insert = "INSERT INTO ClassMember (classID,userID) VALUES (%s,%s);"
        vals = (classID,userID)
        mycursor.execute(class_member_insert,vals)
        mydb.commit()
        print(mycursor.rowcount,"was inserted.")


    def add_class(self, userID,class_name):
        #insert the class into the class table
        sql_insert = "INSERT INTO Class(className) VALUES (%s);"
        vals = ( 
            (class_name,)
        )
        mycursor.execute(sql_insert,vals)
        mydb.commit()
        sql_select =  "SELECT @id:=MAX(classID) FROM Class;"
        mycursor.execute(sql_select)
        classID = mycursor.fetchall()
        sql_classMember_insert = '''INSERT INTO ClassMember (classID,userID) VALUES (%s,%s);'''
        vals = (str(classID[0][0]),str(userID))
        
        mycursor.execute(sql_classMember_insert,vals)
        mydb.commit()
        print("Makes it through first execute.")

    def drop_class(self, userID,class_name):
        #drop class from the class and classMember table
        sql_select = "SELECT classID FROM Class WHERE className = %s;"
        vals = (str(class_name),)
        mycursor.execute(sql_select,vals)
        classID = mycursor.fetchall()
        sql_transaction = '''START TRANSACTION;'''
        mycursor.execute(sql_transaction)
        sql_delete_class_member = '''DELETE FROM ClassMember WHERE classID = %s;''' % classID[0]
        mycursor.execute(sql_delete_class_member)
        sql_delete_class = '''DELETE FROM Class WHERE className = "%s";''' % class_name
        mycursor.execute(sql_delete_class)
        sql_commit = '''COMMIT;'''
        mycursor.execute(sql_commit)
                            
        mydb.commit()
        print("Makes it through first execute.")

    
            

    def add_user(self,discord_user_id, user_name): 
        sql_insert = "INSERT INTO User VALUES (%s,%s);"
        if(self.sql_injection_check(discord_user_id) and self.sql_injection_check(user_name)): 
            vals = (discord_user_id,user_name)
        else: 
            return 0
        mycursor.execute(sql_insert,vals)
        mydb.commit()
        print(mycursor.rowcount,"was inserted.")
        return 1


    def add_question(self, user_id, question_text): 
        sql_insert = "INSERT INTO Question (userID,questionText) VALUES (%s,%s);" 
        if (self.sql_injection_check(user_id) and self.sql_injection_check(question_text)): 
            vals = (user_id,question_text)
        else: 
            return
        mycursor.execute(sql_insert,vals)
        mydb.commit() 
        print(mycursor.rowcount,"was inserted.")


    def answer_question(self,userID,questionID,answerText): 
        sql_insert = "INSERT INTO ANSWER (userID,questionID,answerText) VALUES (%s,%s,%s);"
        if(self.sql_injection_check(userID) and self.sql_injection_check(questionID) and self.sql_injection_check(answerText)):
            vals = (userID,questionID,answerText)
        else: 
            return
        mycursor.execute(sql_insert,vals)
        mydb.commit()
        print(mycursor.rowcount,"was inserted.")


    def get_question(self,userID):
        if(self.sql_injection_check(userID)): 
            vals = (
                (userID,)
            )
        else: 
            return
        rand_question_select = "SELECT * FROM Question WHERE userID = %s ORDER BY RAND() LIMIT 1;"
        mycursor.execute(rand_question_select,vals)
        question = mycursor.fetchall()
        returnList = [question[0][0],question[0][2]]
        return returnList


    def get_answer(questionID): 
        sql_answerid_select = "SELECT answerID FROM Answer WHERE questionID = %s ORDER BY likes DESC;"
        sql_answertext_select = "SELECT answerText FROM Answer WHERE questionID = %s ORDER BY likes DESC;"
        #if(sql_injection_check(questionID)): 
        vals = (
            (questionID,)
        )
        #else: 
        #    return
        mycursor.execute(sql_answerid_select,vals)
        answerIDs = mycursor.fetchall()
        mycursor.execute(sql_answertext_select,vals)
        answerTexts = mycursor.fetchall()
       
        # TODO: TEST RETURNING TUPLE

        return (answerIDs,answerTexts)

    
    #TODO: implement increment of like count for a specific answer
    def increment_likes(self, answer_id):
        print("MAKES IT TO INCREMENT LIKES.")
        sql_update = "UPDATE Answer SET likes = likes + 1 WHERE answerID ="+str(answer_id)+""
        print(sql_update)
        mycursor.execute(sql_update)
        mydb.commit()
        return
   

    # close connection
    def destructor(self):
        # self.db.close()
        return

