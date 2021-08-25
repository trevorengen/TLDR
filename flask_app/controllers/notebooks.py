from flask import json, render_template, redirect, request, session, jsonify, flash, get_flashed_messages
from flask.json import JSONDecoder
from flask_app import app
from flask_app.models.user import User
from flask_app.models.notebook import Notebook

@app.route('/notebooks')
def notebooks():
    if 'user_id' not in session:
        return redirect('/dashboard')
    notebooks = Notebook.get_all_users_notebooks(session)
    if type(notebooks) != list:
        notebooks = []
    return render_template('notebooks.html', notebooks=notebooks)

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
    Notebook.delete_notebook_bullets(data)
    Notebook.delete_notebook(data)
    notebooks = Notebook.get_all_users_notebooks(session)
    notebook_names = []
    for notebook in notebooks:
        notebook_names.append(notebook.name)
    return jsonify(notebook_names)

@app.route('/notebooks/save', methods=['POST'])
def save_to_notebook():
    if 'user_id' not in session:
        flash('You must be logged in to use notebooks.')
        return jsonify('flash error')
    post = request.get_data().decode('utf-8')
    decoder = JSONDecoder()
    post = decoder.decode(post)[0]
    bullets = post['bullets']
    notebook_name = post['notebook_name']
    data = {'name': notebook_name,
            'user_id': session['user_id']}
    notebook = Notebook.get_one_notebook(data)
    data = {'bullets': bullets,
            'notebook_id': notebook.id,
            'user_id': session['user_id'],
            'name': notebook.name}
    Notebook.insert_bullets(data)
    return jsonify('success')
    
@app.route('/notebooks/retrieve', methods=['POST'])
def retrieve_notebook():
    if 'user_id' not in session:
        return redirect('/dashboard')
    notebook_name = request.form['notebook']
    data = {'user_id': session['user_id'],
            'name': notebook_name}
    notebook = Notebook.get_one_notebook(data)
    session['active_notebook'] = notebook.name
    bullets = notebook.bullets
    return jsonify(bullets)