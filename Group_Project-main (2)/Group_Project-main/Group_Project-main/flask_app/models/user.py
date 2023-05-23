import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# PASSWORD_REGEX = re.compile(r'^^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')


class User:
    db = "group_project"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.first_name = db_data["first_name"]
        self.last_name = db_data["last_name"]
        self.email = db_data["email"]
        self.password = db_data["password"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]
        self.posts = []

    @classmethod
    def save(cls, db_data):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        results = connectToMySQL(cls.db).query_db(query, db_data,)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users "
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results: 
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            print("email")
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def verify_register(form_data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.db).query_db(query, form_data)

        if len(form_data['email']) < 1:

            flash('Email cannot be blank.', 'register')
            is_valid = False

        if User.get_by_email(form_data):
            flash("Email is associated with another account", "register")
            is_valid = False

        if not EMAIL_REGEX.match(form_data['email']):

            flash('Invalid email address.', 'register')
            is_valid = False

        if len(form_data['first_name']) < 2:
            flash('First name must be at least 3 characters.',
                  'register')
            is_valid = False

        if len(form_data['first_name']) < 2:
            flash('First name must be at least 2 characters.',
                  'register')
            is_valid = False

        if len(form_data['last_name']) < 2:
            flash('Last name must be at least 2 characters.',
                  'register')
            is_valid = False

        if len(form_data['password']) < 5:
            flash('Password must be at least 5 characters, at least one uppercase letter and one number', 'register')
            is_valid = False

        if form_data['password'] != form_data['confirm_password']:
            flash('Passwords do not match.', 'register')
            is_valid = False

        if not True in (char.isdigit() for char in form_data["password"]):
            flash("Password must contain at least one number")
            is_valid = False

        if not True in (char.isupper() for char in form_data["password"]):
            flash("Password must contain at least one uppercase letter")
            is_valid = False
        return is_valid

    @staticmethod
    def verify_login(form_data):

        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email/password.", "login")
            return False

        user = User.get_by_email(form_data)
        if not user:
            flash("Invalid email.", "login")
            return False
        return user
