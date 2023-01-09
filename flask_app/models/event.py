#krijo nje funksion get event per personin qe eshte ne sesion
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import date, datetime
from flask import flash
class Event:
    db_name='projectdb'
    def __init__(self,data):
        self.id = data['id'],
        self.user_id= data['user_id'],
        self.name = data['name'],
        self.location = data['location'],
        self.date = data['date'],
        self.time= data['time'],
        self.information = data['information'],
        self.playerNr = data['playerNr'],
        self.type = data['type'],
        self.category = data['category']

    @classmethod
    def create_event(cls,data):
        query = 'INSERT INTO events ( user_id, name, location, date, time,information, playerNr, type) VALUES ( %(user_id)s,  %(name)s,  %(location)s, %(date)s, %(time)s, %(information)s, %(playerNr)s,%(type)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getAllEvents(cls):
        query= 'SELECT events.id, events.name, date, time,location, playerNr, COUNT(attendance.id) as attendanceNr, users.id as creator_id, users.name as firstName, users.lastName as lastName  FROM events LEFT JOIN users on events.user_id = users.id LEFT JOIN attendance on attendance.event_id = events.id GROUP BY events.id;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        events= []
        for row in results:
            print(row)
            events.append(row)
        return events

    @classmethod
    def get_event_by_id(cls, data):
        query= 'SELECT * FROM events WHERE events.id = %(event_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def get_event_by_userid(cls, data):
        query= 'SELECT events.id as id FROM events WHERE events.user_id = %(user)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def get_event_joind_users(cls, data):
        query = 'SELECT  distinct users.id, users.name as name, users.lastName FROM users  JOIN events on events.user_id = users.id  JOIN attendance on attendance.user_id = users.id where attendance.event_id=%(event_id)s ;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        usersJoind = []
        for row in results:
            usersJoind.append(row['name'])
        return usersJoind


    @classmethod
    def addJoin(cls, data):
        query= 'INSERT INTO attendance (event_id, user_id) VALUES ( %(event_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeJoin(cls, data):
        query= 'DELETE FROM attendance WHERE event_id = %(event_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroyEvent(cls, data):
        query= 'DELETE FROM events WHERE events.id = %(event_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def deleteAllJoin(cls, data):
        query= 'DELETE FROM attendance WHERE attendance.event_id = %(event_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_event_by_name(cls,data):
        query= 'SELECT events.id, events.name, date, time, playerNr, COUNT(attendance.id) as attendanceNr, users.id as creator_id  FROM events LEFT JOIN users on events.user_id = users.id LEFT JOIN attendance on attendance.event_id = events.id where events.name= %(name)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def get_event_by_type(cls,data):
        query= 'SELECT events.id, events.name, date, time, playerNr, COUNT(attendance.id) as attendanceNr, users.id as creator_id  FROM events LEFT JOIN users on events.user_id = users.id LEFT JOIN attendance on attendance.event_id = events.id where events.type= %(name)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)
    @classmethod
    def get_event_by_creator(cls,data):
        query= 'SELECT events.id, events.name, date, time, playerNr, COUNT(attendance.id) as attendanceNr, users.id as creator_id  FROM events LEFT JOIN users on events.user_id = users.id LEFT JOIN attendance on attendance.event_id = events.id where users.name= %(name)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    # @classmethod
    # def search(data):
        
    #     if(data['category']=='name'):
    #         showEvent=Event.get_event_by_name(name)
    #     if (data['category']=='type'):
    #         showEvent=Event.get_event_by_type(name)
    #     if (data['category']=='location'):
    #         showEvent=Event.get_event_by_location(name)
    #     return showEvent
        

    @staticmethod
    def validate_event(event):
        today = date.today()
        is_valid = True
        if len(event['information']) < 10:
            flash("Event info must be at least 10 characters.", 'information')
            is_valid = False
        if len(event['type']) < 2:
            flash("Event type must be at least 2 characters.", 'type')
            is_valid = False
        if len(event['name']) < 4:
              flash("Event name must be at least 10 characters.", 'name')
              is_valid = False
        # if ((event['playerNr'])< 1) :
        #     flash("Number of players must be at least 2.", 'playerNr')
        #     is_valid = False
        # if ((event['date']) < today) :
        #     flash("You Can create only future events.", 'date')
        #     is_valid = False
        return is_valid
        
