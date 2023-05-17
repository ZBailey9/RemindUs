from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models import chore

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @staticmethod
    def validate_reg(user):
        is_valid = True
        if User.get_user_by_email(user):
            flash("Email already associated with an existing account", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['password'] != user['conf_pw']:
            flash("Passwords must match", "register")
            is_valid = False
        return is_valid

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('chore_schema').query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('chore_schema').query_db(query, data)
        if len(result) < 1:
            return None
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('chore_schema').query_db(query, data)
        if len(result) < 1:
            return None
        return cls(result[0])

    @staticmethod
    def is_user_voter(data):
        query = """SELECT * FROM chores 
                   LEFT JOIN votes ON chores.id = votes.chore_id 
                   LEFT JOIN users ON votes.user_id = users.id 
                   WHERE votes.user_id = %(user_id)s AND votes.chore_id = %(chore_id)s;"""
        result = connectToMySQL('chore_schema').query_db(query, data)
        return len(result) > 0