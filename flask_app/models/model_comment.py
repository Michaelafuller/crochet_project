DATABASE = 'crochet_schema'
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import model_user
from flask_app.models import model_thread


class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.thread_id = data['thread_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.content = data['content']
        self.commented_on = None

    @classmethod
    def create_comment(cls, data):
        query = 'INSERT INTO comments (thread_id, content, user_id) VALUES ( %(thread_id)s, %(content)s, %(user_id)s);'
        
        return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def get_one_comment(cls, data):
    #     query = "SELECT * FROM comments LEFT JOIN users ON users.id = comments.user_id WHERE comments.id = %(id)s;"
    #     results = connectToMySQL(DATABASE).query_db(query, data)

    #     if results:
    #         comment = cls(results[0])
    #         data = {
    #             **results[0],
    #             'id' : results[0]['users.id'],
    #             'created_at' :results[0]['users.created_at'],
    #             'updated_at' : results[0]['users.updated_at']
    #         }

    #         comment.commented_on = model_user.User(data)
    #         print(comment)
    #         return comment
    #     return False

    @classmethod
    def get_comment_by_user(cls, data):
        query = "SELECT * FROM comments LEFT JOIN users ON users.id = comments.user_id WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            comments = []
            for x in results:
                current_comment = cls(x)
                comments.append( current_comment )
                data = {
                    **x,
                    'id' : x['users.id'],
                    'created_at' : x['users.created_at'],
                    'updated_at' : x['users.updated_at']
                }
                current_comment.commented_on = model_user.User(data)


    @classmethod
    def update_one_comment(cls, data):
        query = "UPDATE comments SET content=%(content)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def delete_one_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_comments_with_thread (cls):
        query = "SELECT * FROM comments LEFT JOIN threads ON threads.id = comments.thread_id LEFT JOIN users ON comments.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)

        if results:
            comments = []
            for x in results:
                current_comment = cls(x)
                comments.append( current_comment )
                data = {
                    **x,
                    'id' : x['threads.id'],
                    'content' : x['threads.content'],
                    'created_at' : x['threads.created_at'],
                    'updated_at' : x['threads.updated_at'],
                    'id' : x['users.id'],
                    'created_at' : x['users.created_at'],
                    'updated_at' : x['users.updated_at']
                }
                current_comment.commented_on = model_user.User(data)
            return comments
        return False

    @classmethod
    def get_one_comment(cls, data):
        query = "SELECT * FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        return False



    @staticmethod
    def validate_comment(data):
        is_valid = True

        if len(data['content']) < 10:
            flash('Tell us a little more.', 'err_comment_content')
            is_valid = False

        return is_valid


