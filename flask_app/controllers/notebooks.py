from flask import json, render_template, redirect, request, session, jsonify, flash, get_flashed_messages
from flask.json import JSONDecoder
from flask_app import app
from flask_app.models.user import User
from flask_app.models.notebook import Notebook
from query import query_notebook
from datetime import datetime

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
    if 'name' in request.form:
        data = {'name': request.form['name'],
                'user_id': session['user_id']}
    else:
        data = {'name': request.form['new-name'],
                'user_id': session['user_id']}
    notebooks = Notebook.get_all_users_notebooks(session)
    notebook_names = []
    save = True
    # Check to make sure the name doesn't already exist. 
    # We check here so that we don't muck up the users name
    # incase they want to use weird capitals in places. This allows
    # us to make sure that the name is not the same but allows them to
    # visually still see how they entered it.
    for notebook in notebooks:
        if data['name'].lower() == notebook.name.lower():
            save = False
        notebook_names.append(notebook.name)
    if save:
        Notebook.save_notebook(data)
        notebook_names.append(data['name'])
    return jsonify(notebook_names)

@app.route('/notebooks/update', methods=['POST'])
def update_notebook():
    if 'user_id' not in session:
        return redirect('/dashboard')
    data = {'new_name': request.form['new_name'],
            'old_name': request.form['old_name'],
            'user_id': session['user_id'],
            'updated_at': datetime.now()}
    notebooks = Notebook.get_all_users_notebooks(session)
    notebook_names = []
    update = True
    for notebook in notebooks:
        if data['new_name'].lower() == notebook.name.lower():
            update = False
        if data['old_name'] == notebook.name:
            continue
        else:
            notebook_names.append(notebook.name)
    if update:
        notebook_names.append(data['new_name'])
        Notebook.update_notebook_name(data)
    return jsonify(notebook_names)

@app.route('/notebooks/delete', methods=['POST'])
def delete_notebook():
    if 'user_id' not in session:
        flash('You must be logged in to manage notebooks.')
        return jsonify('flash error')
    if 'nbName' in request.form:
        data = {'name': request.form['nbName'],
                'user_id': session['user_id']}
    else:
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

@app.route('/notebooks/query', methods=['POST'])
def ask_to_notebook():
    if 'user_id' not in session:
        return redirect('/dashboard')
    if 'active_notebook' not in session:
        return jsonify('Valid notebook not found.')
    query = request.form['query']
    notebook_name = session['active_notebook']
    data = {
            'user_id': session['user_id'],
            'name': notebook_name
    }
    notebook = Notebook.get_one_notebook(data)
    context = ' '.join(notebook.bullets)
    answer = query_notebook(query, context)
    return jsonify(answer)

@app.route('/notebooks/addbullet', methods=['POST'])
def add_bullet():
    if 'user_id' not in session:
        return redirect('/dashboard')
    if 'active_notebook' not in session:
        return jsonify('Valid notebook not found.')
    bullet = request.form['bullet']
    data = {'name': session['active_notebook'],
            'user_id': session['user_id']}
    notebook = Notebook.get_one_without_bullets(data)
    bullet_data = {'bullet': bullet,
                    'notebook_id': notebook.id}
    result = Notebook.insert_one_bullet(bullet_data)
    if result == False:
        return jsonify('Error adding bullet.')
    return jsonify('Complete')

@app.route('/notebooks/deletebullets', methods=['POST'])
def delete_all_bullets():
    if 'user_id' not in session:
        return redirect('/dashboard')
    if 'active_notebook' not in session:
        return jsonify('Valid notebook not found.')
    data = {'name': session['active_notebook'],
    'user_id': session['user_id'],}
    notebook = Notebook.get_one_without_bullets(data)
    result = Notebook.delete_notebook_bullets({'id': notebook.id})
    if result == False:
        return jsonify('Error deleting bullets.')
    return jsonify('Complete')