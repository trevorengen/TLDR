from flask import render_template, redirect, request, session, jsonify
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from summarize import other_to_text, summarize
import os
from summarize import pdfToText, txt_to_text, other_to_text

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
    return render_template('dashboard.html', summary=summary)

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
def login_register():
    return render_template('logreg.html')