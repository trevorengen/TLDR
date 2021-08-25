from flask import render_template, redirect, request, session, jsonify, flash, get_flashed_messages
from flask_app import app
from flask_app.models.user import User
from flask_app.models.notebook import Notebook
from flask_bcrypt import Bcrypt
from summarize import other_to_text, summarize
import os
from summarize import pdfToText, txt_to_text, other_to_text

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'summary' in session and 'summarize' in session:
        summary = session['summary']
        summarize = session['summarize']
    else:
        session['summary'] = ''
        session['summarize'] = ''
        summary = ''
    if 'user_id' in session:
        user = User.get_user(session)
        notebooks = Notebook.get_all_users_notebooks(session)
    else:
        user = None
        notebooks = None
    return render_template('dashboard.html', summary=summary, user=user, notebooks=notebooks)

@app.route('/summarize', methods=['POST'])
def summarize_text():
    # First we check if there was a file upload
    if request.files['file-upload'].filename != '':
        file = request.files['file-upload']
        file_tup = os.path.splitext(file.filename)
        # Once we know a file is uploaded we deduce what the type is.
        if file_tup[1] == '.pdf':
            to_summarize = pdfToText(file)
        if file_tup[1] == '.txt':
            to_summarize = txt_to_text(file)
        else:
            to_summarize = other_to_text(file)

    # If there is no file upload then we just work with the textarea and assume that
    # the user has pasted something in.
    else:
        to_summarize = request.form['summarize']
    output = summarize(to_summarize)
    session['summary'] = output
    session['summarize'] = to_summarize
    return jsonify(output)

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('logreg.html')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('logreg.html')

@app.route('/user/login', methods=['POST'])
def login_user():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }
    if not User.validate_login(data):
        return jsonify(get_flashed_messages())
    if User.get_user(request.form) != False:
        user = User.get_user(request.form)
    else:
        flash('Invalid email or password.')
        return jsonify(get_flashed_messages())
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password.')
        return jsonify(get_flashed_messages())
    else:
        session['user_id'] = user.id
        return jsonify('connect')

@app.route('/user/register', methods=['POST'])
def register_user():
    if not User.validate_registration(request.form):
        return jsonify(get_flashed_messages())
    pass_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pass_hash,
    }
    session['user_id'] = User.save(data)
    return jsonify('connect')

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/dashboard')