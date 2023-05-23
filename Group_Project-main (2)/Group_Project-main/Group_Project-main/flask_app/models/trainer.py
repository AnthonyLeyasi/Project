from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Trainer:
    db = "group_project"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.city = data['city']
        self.gym = data['gym']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trainers JOIN users on trainers.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        trainers = []
        for row in results:
            this_trainer = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_trainer.creator = user.User(user_data)
            trainers.append(this_trainer)
        return trainers

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM trainers JOIN users on trainers.user_id = users.id WHERE trainers.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(id)
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO trainers (first_name, last_name, user_id, city, gym, description, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(user_id)s, %(city)s, %(gym)s, %(description)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, form_data):
        query = "UPDATE trainers SET first_name=%(first_name)s, last_name=%(last_name)s,  city=%(city)s, gym=%(gym)s, description=%(description)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, form_data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM trainers WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_trainer(form_data):
        is_valid = True
        query = "SELECT * FROM trainers WHERE first_name = %(first_name)s"
        results = connectToMySQL(Trainer.db).query_db(query, form_data)
        if len(form_data['first_name']) < 3:
            flash("first_name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash("last_name must be at least 3 characters long.")
            is_valid = False
        return is_valid
