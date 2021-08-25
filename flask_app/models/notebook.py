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
        query = 'SELECT * FROM notebooks '
        query += 'WHERE notebooks.name = %(name)s AND notebooks.user_id = %(user_id)s;'
        result = connectToMySQL(DB).query_db(query, data)
        if result == False:
            return False
        notebook = cls(result[0])
        query = 'SELECT bullets.id, bullets.bullet FROM bullets WHERE notebook_id = %(notebook_id)s;'
        bullets = connectToMySQL(DB).query_db(query, {'notebook_id': notebook.id})
        if bullets == False:
            return notebook
        for bullet in bullets:
            notebook.bullets.append(bullet['bullet'])
        return notebook

    @classmethod
    def get_one_without_bullets(cls, data):
        query = 'SELECT * FROM notebooks WHERE notebooks.name = %(name)s AND notebooks.user_id = %(user_id)s;'
        result = connectToMySQL(DB).query_db(query, data)
        if result == False:
            return False
        notebook = cls(result[0])
        return notebook


    @classmethod
    def get_all_users_notebooks(cls, data):
        query = 'SELECT * FROM notebooks '
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

    # Assumes bullets are passed as an array.
    @classmethod
    def insert_bullets(cls, data):
        notebook = Notebook.get_one_notebook(data)
        results = None
        for bullet in data['bullets']:
            if bullet in notebook.bullets:
                continue
            else:
                new_data = {'bullet': bullet, 'notebook_id': notebook.id}
                query = 'INSERT INTO bullets (bullet, notebook_id) VALUES (%(bullet)s, %(notebook_id)s);'
                results = connectToMySQL(DB).query_db(query, new_data)
        if results == None:
            return False
        return results

    @classmethod
    def delete_notebook_bullets(cls, data):
        if ('id' not in data):
            notebook = Notebook.get_one_notebook(data)
            new_data = {'id': notebook.id}
        else:
            new_data = data
        query = 'DELETE FROM bullets WHERE notebook_id = %(id)s;'
        results = connectToMySQL(DB).query_db(query, new_data)
        return results

    @classmethod
    def insert_one_bullet(cls, data):
        query = 'INSERT INTO bullets (bullet, notebook_id) VALUES(%(bullet)s, %(notebook_id)s);'
        results = connectToMySQL(DB).query_db(query, data)
        return results