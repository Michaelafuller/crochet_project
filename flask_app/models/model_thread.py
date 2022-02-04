DATABASE = 'crochet_schema'
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import model_user

class Thread:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.posted_by = None

    @classmethod
    def create_thread(cls, data):
        query = 'INSERT INTO threads (title, content, user_id) VALUES ( %(title)s, %(content)s, %(user_id)s);'
        
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one_thread(cls, data):
        query = "SELECT * FROM threads LEFT JOIN users ON users.id = threads.user_id WHERE threads.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            thread = cls(results[0])
            data = {
                **results[0],
                'id' : results[0]['users.id'],
                'created_at' :results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }

            thread.posted_by = model_user.User(data)
            print(thread)
            return thread
        return False

    @classmethod
    def get_thread_by_user(cls, data):
        query = "SELECT * FROM threads LEFT JOIN users ON users.id = threads.user_id WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            threads = []
            for x in results:
                current_thread = cls(x)
                threads.append( current_thread )
                data = {
                    **x,
                    'id' : x['users.id'],
                    'created_at' : x['users.created_at'],
                    'updated_at' : x['users.updated_at']
                }
                current_thread.posted_by = model_user.User(data)


    @classmethod
    def update_one_thread(cls, data):
        query = "UPDATE threads SET title=%(title)s, content=%(content)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def delete_one_thread(cls, data):
        query = "DELETE FROM threads WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_threads_with_user (cls):
        query = "SELECT * FROM threads LEFT JOIN users ON users.id = threads.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            threads = []
            for x in results:
                current_thread = cls(x)
                threads.append( current_thread )
                data = {
                    **x,
                    'id' : x['users.id'],
                    'created_at' : x['users.created_at'],
                    'updated_at' : x['users.updated_at']
                }
                current_thread.posted_by = model_user.User(data)

            print(threads)
            return threads
        return False

    @staticmethod
    def validate_thread(data):
        is_valid = True

        if len(data['title']) < 4:
            flash('Title should be longer than 4 characters.', 'err_thread_title')
            is_valid = False

        if len(data['content']) < 10:
            flash('Be more specific. Tell us what this thread is all about.', 'err_thread_content')
            is_valid = False

        return is_valid


