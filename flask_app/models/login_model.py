from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import db, app
import re
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTERS_REGAX = re.compile(r'^[a-zA-Z]{3,}$')
PASSWORD_REGAX = re.compile(r'^[a-zA-Z0-9.#?!@$ %^&*-]{8,}$')

# password regas to check if it has
# minimum eight characters, at least one upper case English letter,
# one lower case English letter, one number and one special character
# PASSWORD_REGAX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # CREATE
    @classmethod
    def create(cls, data):
        query = '''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        '''
        return connectToMySQL(db).query_db(query, data)

    # Get row by email
    @classmethod
    def get_by_email(cls, email):
        query = '''
            SELECT * FROM users WHERE email = %(email)s;
        '''
        data = {
            'email': email
        }
        # here it will return a list of dict
        results = connectToMySQL(db).query_db(query, data)
        # we only need the first dictionary
        # return results[0]
        if results:
            return cls(results[0])
        return False

    # Get one
    @classmethod
    def get_one(cls, user_id):
        query = '''
            SELECT * FROM users WHERE id = %(id)s;
        '''
        data = {
            'id': user_id
        }
        # here it will return a list of dict
        results = connectToMySQL(db).query_db(query, data)
        # we only need the first dictionary
        # return results[0]
        if results:
            return cls(results[0])
        return False

    # register validation
    @staticmethod
    def validate_registration(data):
        is_valid = True
        if not LETTERS_REGAX.match(data['first_name']):
            flash("First name must be at least 3 characters and letters only")
            is_valid = False
        if not LETTERS_REGAX.match(data['last_name']):
            flash("Last name must be at least 3 characters and letters only")
            is_valid = False
        # if I have time, check if email is unique
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!!!")
            is_valid = False
        else:  # check if the email is unique
            potential_user = User.get_by_email(data['email'])
            if potential_user:
                flash('email already exists in db')
                is_valid = False
        if not PASSWORD_REGAX.match(data['password']):
            flash("Password must be at least 8 characters")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("The confirm password must be the same as the password")
            is_valid = False
        return is_valid
