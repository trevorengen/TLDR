from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from summarize import summarize
import os
from summarize import pdfToText

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
    # If there is no file upload then we just work with the textarea and assume that
    # the user has pasted something in.
    else:
        to_summarize = request.form['summarize']
    output = summarize(to_summarize)
    session['summary'] = output
    session['summarize'] = to_summarize
    return redirect('/dashboard')