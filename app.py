from flask import Flask, flash, redirect, render_template, request, session, abort
from pymongo import MongoClient as mon
from werkzeug import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
db = mon()['blockchain']

@app.route('/do_login', methods=['POST'])
def do_login():
    if request.form['username']!='' and request.form['password']!='':
        users = db.users
        user = users.find_one({'username':request.form['username']})
        if check_password_hash(user['password'], request.form['password']):
            session['loggedIn']=True
            session['name']= user['name']
            session['role']= user['role']
    return home()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/do_signup', methods=['POST'])
def do_signup():    
    if request.form['username']!='' and request.form['password']!='' and request.form['role'] and request.form['name']!='':
        users = db['users']
        data = {'name':request.form['name'], 'username': request.form['username'], 'password': generate_password_hash(request.form['password'], salt_length=8), 'role': request.form['role']}
        users.save(data)
        session['loggedIn']=True
        session['name']=request.form['name']
        session['role']=request.form['role']
    return home()

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/')
def home():
    if not session.get('loggedIn'):
        return render_template('nothome.html')
    else:
        return render_template('home.html', loggedIn = session['loggedIn'], name = session['name'])

@app.route("/logout", methods=['GET'])
def logout():
    session['loggedIn'] = False
    return home()

# @app.route('/copy')
# def copy():


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

# flask run --host=10.20.202.61 --port=8080
# ni.ifaddresses('en0')[2][0]['addr'] for mac