DATABASE = 'crochet_schema'
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, bcrypt
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, pw) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(pw)s );'
        
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)

        users = []
        for user in results:
            users.append( cls(user) )

        return users


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        user_called = connectToMySQL(DATABASE).query_db(query, data)
        if user_called:
            return cls(user_called[0])
        return False


    @classmethod
    def update_one(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash('First name must have more than 2 characters', 'err_user_first_name')
            is_valid = False        
        
        if len(data['last_name']) < 2:
            flash('Last name must have more than 2 characters', 'err_user_last_name')
            is_valid = False

        if len(data['email']) < 2:
            flash('Email must have more than 2 characters', 'err_user_email')
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address. Please use the correct format: name@domain.com', 'err_user_email')
            is_valid = False

        else:
            user = User.get_one_by_email(data)
            if user:
                flash("Email is already in use", 'err_user_email')
                is_valid = False

        if len(data['pw']) < 7:
            flash('Invalid password. Try a stronger password.', 'err_user_pw')
            is_valid = False

        if len(data['confirm_pw']) < 2:
            flash('Invalid password. Try a stronger password.', 'err_user_confirm_pw')
            is_valid = False

        elif data['confirm_pw'] != data['pw']:
            flash('Passwords do not match', 'err_user_confirm_pw')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(data):
        is_valid = True

        if len(data['pw']) < 2:
            flash('Invalid Credentials.', 'err_user_pw_login')
            is_valid = False

        else:
            user = User.get_one_by_email(data)
            if user:
                if not bcrypt.check_password_hash(user.pw, data['pw']):
                    flash('Invalid Credentials', 'err_user_pw_login')
                    is_valid = False
                else:
                    session['uuid'] = user.id
            if not user:
                flash('No account with this email exists', 'err_user_pw_login')
                is_valid = False

        if len(data['email']) < 2:
            flash('Email must have more than 2 characters', 'err_user_email_login')
            is_valid = False

        elif not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address. Please use the correct format: name@domain.com', 'err_user_email_login')
            is_valid = False


        return is_valid

    @staticmethod
    def validate_user_update(data):
        is_valid = True

        if len(data['first_name']) < 2:
            flash('First name must have more than 2 characters', 'err_user_first_name')
            is_valid = False        
        
        if len(data['last_name']) < 2:
            flash('Last name must have more than 2 characters', 'err_user_last_name')
            is_valid = False

        if len(data['email']) < 2:
            flash('Email must have more than 2 characters', 'err_user_email')
            is_valid = False

        return is_valid
