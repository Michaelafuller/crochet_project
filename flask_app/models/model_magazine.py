DATABASE = 'fuller_exam'
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import model_user

class Magazine:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.subscribed_by = None

    @classmethod
    def create_magazine(cls, data):
        query = 'INSERT INTO magazines (title, description, user_id) VALUES ( %(title)s, %(description)s, %(user_id)s);'
        
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one_magazine(cls, data):
        query = "SELECT * FROM magazines LEFT JOIN users ON users.id = magazines.user_id WHERE magazines.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            magazine = cls(results[0])
            data = {
                **results[0],
                'id' : results[0]['users.id'],
                'created_at' :results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }

            magazine.subscribed_by = model_user.User(data)
            print(magazine)
            return magazine
        return False

    @classmethod
    def get_magazine_by_user(cls, data):
        query = "SELECT * FROM magazines LEFT JOIN users ON users.id = magazines.user_id WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            magazines = []
            for x in results:
                current_magazine = cls(x)
                magazines.append( current_magazine )
                data = {
                    **x,
                    'id' : x['users.id'],
                    'created_at' : x['users.created_at'],
                    'updated_at' : x['users.updated_at']
                }
                current_magazine.subscribed_by = model_user.User(data)


    @classmethod
    def update_one_magazine(cls, data):
        query = "UPDATE magazines SET title=%(title)s, description=%(description)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def delete_one_magazine(cls, data):
        query = "DELETE FROM magazines WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_magazines_with_user (cls):
        query = "SELECT * FROM magazines LEFT JOIN users ON users.id = magazines.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            magazines = []
            for x in results:
                current_magazine = cls(x)
                magazines.append( current_magazine )
                data = {
                    **x,
                    'id' : x['users.id'],
                    'created_at' : x['users.created_at'],
                    'updated_at' : x['users.updated_at']
                }
                current_magazine.subscribed_by = model_user.User(data)

            print(magazines)
            return magazines
        return False

    @staticmethod
    def validate_magazine(data):
        is_valid = True

        if len(data['title']) < 4:
            flash('Title should be longer than 4 characters.', 'err_magazine_title')
            is_valid = False

        if len(data['description']) < 10:
            flash('Be more specific. Tell us what this magazine is all about.', 'err_magazine_description')
            is_valid = False

        return is_valid


