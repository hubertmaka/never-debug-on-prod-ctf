import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, make_response

os.environ["WERKZEUG_DEBUG_PIN"] = "564-678-923"
os.environ["FLAG_PATH"] = f'{Path(__name__).parent / "secret" / "in-this-file-there-are-no-flags.txt"}'
os.environ["FLASK_DEBUG"] = "1"
app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'session'
app.session_cookie_name = app.config['SESSION_COOKIE_NAME']
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecret')
app.config['SESSION_TYPE'] = 'filesystem'
ADMIN_USER = 'admin'
ADMIN_PASS = 'matrix'

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hint')
def hint():
    return render_template('hint.html', user=ADMIN_USER)


@app.route('/login', methods=['GET', 'POST'])
def login():
    err = None
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if pwd == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            err = 'Try again... Next hint - algebra nightmare'
    return render_template('login.html', error=err)


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    endpoints = ['/hint', '/admin', '/api/secret-endpoint']
    return render_template('admin.html', endpoints=endpoints)


@app.route('/api/secret-endpoint')
def secret_endpoint():
    img_url = url_for('static', filename='cookie-monster.jpeg')
    response = make_response(f"<html><body><h1>Monster Cookie!</h1><img src='{img_url}' /></body></html>")
    cookies = {
        'session_info': 'user=guest',
        'console_pin': os.getenv("WERKZEUG_DEBUG_PIN"),
    }
    for k, v in cookies.items():
        response.set_cookie(k, v)
    return response

