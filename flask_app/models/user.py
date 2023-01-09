from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    db_name='projectdb'
    def __init__(self,data):
        self.id = data['id'],
        self.name = data['name'],
        self.lastName = data['lastName'],
        self.email = data['email'],
        self.password = data['password'],
        self.birthdate = data['birthdate'],
        self.photoName = data['photoName']
    
    @classmethod
    def getAllUsers(cls):
        query= 'SELECT * FROM users;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        users= []
        for row in results:
            users.append(row)
        return users
    
    @classmethod
    def get_user_by_id(cls, data):
        query= 'SELECT * FROM users WHERE users.id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]
        
    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]
        

    @classmethod
    def get_all_user_info(cls, data):
        query= 'SELECT * FROM users LEFT JOIN posts on events.user_id = users.id WHERE users.id = %(user_id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        events = []
        for row in results:
            events.append(row)
        return events
    
    #Class Method to create a user
    @classmethod
    def create_user(cls,data):
        query = 'INSERT INTO users ( name, lastName, email, password, birthdate) VALUES (  %(name)s, %(lastName)s, %(email)s, %(password)s, %(birthdate)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    #Merr id e eventeve qe nje person i ka bere join
    @classmethod
    def get_logged_user_joind_events(cls, data):
        query = 'SELECT event_id as id FROM attendance LEFT JOIN users on attendance.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        eventsJoind = []
        for row in results:
            eventsJoind.append(row['id'])
        return eventsJoind

    @classmethod
    def update_user(cls,data):
        query = 'UPDATE users SET name=%(name)s, lastName=%(lastName)s, password=%(password)s WHERE id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def profilePic(cls,data):
        query = 'UPDATE users SET photoName=%(photoName)s where id = %(user_id)s ;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['name']) < 3:
            flash("Name must be at least 3 characters.", 'name')
            is_valid = False
        if len(user['lastName']) < 3:
            flash("Last name be at least 3 characters.", 'lastName')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password be at least 8 characters.", 'passwordRegister')
            is_valid = False
        if user['confirmpassword'] != user['password']:
            flash("Password do not match!", 'passwordConfirm')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit_user(user):
        is_valid = True
        if len(user['name']) < 3:
            flash("Name must be at least 3 characters.", 'name')
            is_valid = False
        if len(user['lastName']) < 3:
            flash("Last name be at least 3 characters.", 'lastName')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password be at least 8 characters.", 'password')
            is_valid = False
        return is_valid