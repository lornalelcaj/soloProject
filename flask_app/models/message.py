from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
class Message:
    db_name='projectdb'
    def __init__(self,data):
        self.id = data['id'],
        self.user_id= data['user_id'],
        self.event_id = data['event_id'],
        self.content = data['content']

    @classmethod
    def create_message(cls,data):
        query = 'INSERT INTO messages  ( user_id, event_id, content) VALUES ( %(user_id)s,  %(event_id)s,  %(content)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getAllMessages(cls):
        query= 'SELECT messages.id, messages.content,  messages.user_id , messages.event_id, users.name as firstName, users.lastName as lastName  FROM messages LEFT JOIN users on messages.user_id = users.id LEFT JOIN events on messages.event_id = events.id ;'
        results =  connectToMySQL(cls.db_name).query_db(query)
        messages= []
        for row in results:
            print(row)
            messages.append(row)
        return messages
        
    @staticmethod
    def validate_message(message):
        is_valid = True
        if len(message['content']) < 2:
            flash("Message content must be at least 2 characters.", 'content')
            is_valid = False
        return is_valid