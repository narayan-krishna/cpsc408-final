# db_utils.py
# implements main database utilities with mysql queries

import os
from turtle import update
import mysql.connector
import random
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')

mydb = mysql.connector.connect(host="localhost",
user="root",
password=DB_PASSWORD,
auth_plugin='mysql_native_password',
database="WizBot")
#print(mydb)


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


    def drop_class(self, class_name):
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

    def commit(self): 
        sql_commit = '''COMMIT;'''
        mycursor.execute(sql_commit)
        mydb.commit()
    
    def rollback(self): 
        sql_commit = '''ROLLBACK;'''
        mycursor.execute(sql_commit)
        mydb.commit()


    # WARNING: DOUBLE CHECK THIS FUNCTION FOR NAMING ISSUES ACROSS DATABASES
    # this should also take self as a param but throws a warn?
    def select_class_names():
        sql_select_classnames = f'SELECT className FROM class;'
        mycursor.execute(sql_select_classnames)
        class_names = mycursor.fetchall();
        return class_names


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


    # NOTE: this question should take self as a parameter but seems to work without it
    def get_answer(questionID): 
        #NOTE: can do in one query?
        sql_answerid_select = "SELECT answerID FROM Answer WHERE questionID = %s ORDER BY likes DESC;"
        sql_answertext_select = "SELECT answerText FROM Answer WHERE questionID = %s ORDER BY likes DESC;"

        #sql_answer_select = "SELECT answerID, (SELECT answerText FROM Answer WHERE questionID = %s ORDER BY likes DESC) FROM Answer WHERE questionID = %s ORDER BY likes DESC;"
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

        #mycursor.execute(sql_answer_select, questionID, questionID) #might need to have question id in vals twice to work properly
        #answers = mycursor.fetchall()
       
        # TODO: TEST RETURNING TUPLE

        return (answerIDs,answerTexts)


    # query to allow users to update an answer
    def update_answer(self, userID,answerID,newAnswerText): 
        update_query = "UPDATE Answer SET answerText = \""+str(newAnswerText)+"\" WHERE answerID = "+str(answerID)+" AND userID = "+userID+";"
        mycursor.execute(update_query)
        mydb.commit()

    
    # increments likes of a specific answer when the answer is liked
    def increment_likes(self, answer_id):
        print("MAKES IT TO INCREMENT LIKES.")
        sql_update = "UPDATE Answer SET likes = likes + 1 WHERE answerID ="+str(answer_id)+""
        print(sql_update)
        mycursor.execute(sql_update)
        mydb.commit()
        return


    # writes a table to a given a file in a csv format
    def write_table(self, file, table):
        sql_get_all = f'SELECT * FROM {table};'
        mycursor.execute(sql_get_all)
        select = mycursor.fetchall()
        file.write(table + ',\n')
        for tuples in select:
            for value in tuples:
                file.write(str(value) + ',')
            file.write('\n')
        file.write('\n')


    # writes all tables to file
    # PERF: reimplement this with a join??
    def generate_csv(self):
        file = open("quizbot_report.csv", "w")
        self.write_table(file, "user")
        self.write_table(file, "class")
        self.write_table(file, "classmember")
        self.write_table(file, "question")
        self.write_table(file, "answer")
        return

    #Get the top answer that someone has written
    def get_answers_per_question(self): 
        query = "SELECT COUNT(answerID),questionID FROM Answer GROUP BY questionID;"
        mycursor.execute(query)
        select = mycursor.fetchall()
        return select


    # close connection
    def destructor(self):
        mydb.close()
        return

