from flask_app.config.mysqlcontroller import connectToMySQL
import re
from flask import flash

EMAIL_CHECK = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
CAPS = re.compile(r'[A-Z]')
NUMS = re.compile(r'[0-9]')
DB = 'tldr_schema'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_registration(input):
        is_valid = True
        if len(input['first_name']) < 3 or len(input['last_name']) < 3:
            flash('First and last name must be at least 3 characters.')
            is_valid = False
        if not EMAIL_CHECK.match(input['email']):
            flash('Invalid email address.')
            is_valid = False
        if len(input['password']) < 6:
            flash('Password must be at least 6 characters.')
            is_valid = False
        elif not CAPS.search(input['password']) or not NUMS.search(input['password']):
            flash('Password must contain at least one capital letter AND one number.')
            is_valid = False
        elif input['password'] != input['confirm-password']:
            flash('Passwords don\'t match.')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(input):
        is_valid = True
        if not EMAIL_CHECK.match(input['email']):
            flash('Please enter a valid email.')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) '
        query += 'VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        user_id = connectToMySQL(DB).query_db(query, data)
        return user_id

    @classmethod
    def update(cls, data, option='p'):
        addComma = False
        query = 'UPDATE users SET '
        if option == 'p':
            query += 'password = %(password)s '
            addComma = True
        if option == 'e':
            if addComma:
                query += ', '
            query += 'email = %(email)s '
            addComma = True
        if option == 'n':
            if addComma:
                query += ', '
            query += 'first_name = %(first_name)s, last_name = %(last_name)s '
        query += 'WHERE id == %(id)s;'
        result = connectToMySQL(DB).query_db(query, data)
        return result

    @classmethod
    def get_user(cls, data):
        if 'id' in data:
            query = 'SELECT * FROM users WHERE id = %(id)s;'
        if 'user_id' in data:
            query = 'SELECT * FROM users WHERE id = %(user_id)s;'
        if 'email' in data:
            query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DB).query_db(query, data)
        if len(results) == 0:
            return False
        user = cls(results[0])
        return user

    @classmethod
    def delete_user(cls, data):
        query = 'DELETE FROM users WHERE id = %(id)s AND password = %(password)s;'
        did_delete = connectToMySQL(DB).query_db(query, data)
        return did_delete 

