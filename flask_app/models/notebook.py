from flask_app.config.mysqlcontroller import connectToMySQL
import re
from flask import flash

DB = 'tldr_schema'

class Notebook:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.bullets = []

    @staticmethod
    def validate_name(input):
        is_valid = True
        notebooks = Notebook.get_all_users_notebooks(input)
        notebook_names = []
        for notebook in notebooks:
            notebook_names.append(notebook.name)
        if len(input['name']) < 1:
            flash('Name cannot be empty.')
            is_valid = False
        if input['name'] in notebook_names:
            flash('Notebook already exists.')
            is_valid = False
        return is_valid

    @classmethod
    def save_notebook(cls, data):
        query = 'INSERT INTO notebooks (name, user_id) VALUES (%(name)s, %(user_id)s);'
        result = connectToMySQL(DB).query_db(query, data)
        return result

    @classmethod
    def delete_notebook(cls, data):
        query = 'DELETE FROM notebooks WHERE name = %(name)s AND user_id = %(user_id)s;'
        result = connectToMySQL(DB).query_db(query, data)
        return result

    @classmethod
    def get_one_notebook(cls, data):
        query = 'SELECT * FROM notebooks LEFT JOIN bullets ON notebooks.id = bullets.notebook_id '
        query += 'WHERE notebooks.name = %(name)s AND notebooks.user_id = %(user_id)s;'
        result = connectToMySQL(DB).query_db(query, data)
        notebook = cls(result[0])
        return notebook

    @classmethod
    def get_all_users_notebooks(cls, data):
        query = 'SELECT * FROM notebooks LEFT JOIN bullets ON notebooks.id = bullets.notebook_id '
        query += 'WHERE notebooks.user_id = %(user_id)s;'
        results = connectToMySQL(DB).query_db(query, data)
        if results == False:
            return results
        notebooks = []
        for notebook in results:
            notebooks.append(cls(notebook))
        return notebooks

    @classmethod
    def get_all_bullets(cls, data):
        query = 'SELECT bullet FROM bullets WHERE notebook_id = %(id)s;'
        results = connectToMySQL(DB).query_db(query, data)
        return results