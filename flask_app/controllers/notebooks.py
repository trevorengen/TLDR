from flask import json, render_template, redirect, request, session, jsonify, flash, get_flashed_messages
from flask_app import app
from flask_app.models.user import User
from flask_app.models.notebook import Notebook

@app.route('/notebooks')
def notebooks():
    return render_template('notebooks.html')

@app.route('/notebooks/add', methods=['POST'])
def add_notebook():
    if 'user_id' not in session:
        flash('You must be logged in to save notebooks.')
        return jsonify('flash error')
    data = {'name': request.form['new-name'],
            'user_id': session['user_id']}
    Notebook.save_notebook(data)
    notebooks = Notebook.get_all_users_notebooks(session)
    notebook_names = []
    for notebook in notebooks:
        notebook_names.append(notebook.name)
    return jsonify(notebook_names)

@app.route('/notebooks/delete', methods=['POST'])
def delete_notebook():
    if 'user_id' not in session:
        flash('You must be logged in to manage notebooks.')
        return jsonify('flash error')
    data = {'name': request.form.get('notebook-select'),
            'user_id': session['user_id']}
    Notebook.delete_notebook(data)
    notebooks = Notebook.get_all_users_notebooks(session)
    notebook_names = []
    for notebook in notebooks:
        notebook_names.append(notebook.name)
    return jsonify(notebook_names)