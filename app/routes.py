#microblog routes.py temporary save in case things go south of the border 

#favicon: https://i.pinimg.com/originals/06/15/71/06157196656587bc901c6e8bf4848fe1.jpg

from flask import Flask, render_template, request, session, redirect, url_for, g, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_socketio import SocketIO
from app import app
from app.forms import LoginForm
from win32gui import GetWindowText, GetForegroundWindow
import threading
from datetime import datetime
import uiautomation as auto
import socket
import pickle
import time
import pandas as pd
import requests
import pprint
import json
from urllib.request import urlopen

class User:
    def __init__(self, id, username, password, email):
        self.id = id
        self.username= username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=0, username='Z', password='z', email='z@gmail.com'))
users.append(User(id=1, username='Anthony', password='password', email='anthony@gmail.com'))
users.append(User(id=2, username='Rebecca', password='magicunicorn', email='rebecca.bi@st-agnes.org'))
users.append(User(id=3, username='Carlos', password='simple', email='carlos@gmail.com'))

#@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0] ######
        g.user = user
        
#print(users[1].id)

headers = {
    'Content-type': 'application/json',
}

data = '{"title":"what"}' #lol what 

#with urlopen('http://localhost:5000/todo/api/v1.0/tasks') as resp:
#    project_info = json.load(resp)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/websites')
def websites():
    before_request()
    if not g.user:
        return render_template('login.html', title='Sign In')
    user = g.user
    response = requests.get('https://magicunicorn.herokuapp.com/todo/api/v1.0/tasks', headers=headers, data=data)
    response = response.json()
    #response = '[' + str(response) + ']'
    #response = list(response)
    return render_template('websites.html', title='Websites', response=response, user=user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)
        
        username = request.form['username']
        password = request.form['password']

        try:
            user = [x for x in users if x.username == username][0] #####
            if user and user.password == password: 
                session['user_id'] = user.id
                before_request()
                return redirect(url_for('profile'))
            else:
                flash("Incorrect username or password, please try again.")
        except:
            flash("Incorrect username or password, please try again.")

        return redirect(url_for('login')) #no text, just back to login

    before_request()
    return render_template('login.html', title='Sign In')

@app.route('/profile')
def profile():
    before_request()
    if not g.user:
        return render_template('login.html', title='Sign In')    
    flash("Successfuly logged in! Welcome!")
    return render_template('profile.html', title='Your Profile')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        session.pop('user_id', None)
        newuser = request.form['username']
        newpass = request.form['password']
        newemail = request.form['email']

        idcount = users[-1].id + 1

        for i in users:
            if newuser in i.username:
                flash("Username already taken, please try registering another one.")
                return render_template('register.html', title='Register')

        users.append(User(idcount, username=newuser, password=newpass, email=newemail))
        user = [x for x in users][0]
        session['user_id'] = user.id
        return redirect(url_for('login'))
        
    return render_template('register.html', title='Register')

@app.route('/apps')
def apps():
    before_request()
    user = g.user
    response = requests.get('https://magicunicorn.herokuapp.com/todo/api/v1.0/tasks', headers=headers, data=data)
    response = response.json()
    return render_template('apps.html', title='Apps', response=response, user=user)

@app.route('/domains')
def domains():
    before_request()
    if not g.user:
        return render_template('login.html', title='Sign In')
    user = g.user
    response = requests.get('https://magicunicorn.herokuapp.com/todo/api/v1.0/tasks', headers=headers, data=data)
    response = response.json()
    return render_template('domains.html', title='Domains', response=response, user=user)

@app.route('/block', methods = ['GET', 'POST'])
def block():
    before_request()
    if not g.user:
        return render_template('login.html', title='Sign In')
    user = g.user
    
    response2 = requests.get('https://magicunicorn2.herokuapp.com/todo/api/v1.0/tasks', headers=headers, data=data)
    response2 = response2.json()
    
    if request.method == 'POST':
        starttime = request.form['starttime']
        endtime = request.form['endtime']
        website = request.form['website']

        sentdata = 'website5858: ' + starttime + '-' + endtime + '*' + website

        headerss = {
        'Content-type': 'application/json',
        }
        dataa = '{"username":"%f", "title":"%s"}'%(g.user.id, sentdata)
        response = requests.post('http://localhost:5858/todo/api/v1.0/tasks', headers=headerss, data=dataa.encode('utf-8'))
    
        return render_template('block.html', title='Block', user=user, response2=response2)
    
    return render_template('block.html', title='Block', user=user, response2=response2)

@app.route('/error')
def error():
    return render_template('error.html', title='Error')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,threaded=True)

'''
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
from win32gui import GetWindowText, GetForegroundWindow
import threading
from datetime import datetime
import uiautomation as auto
import socket
import pickle
import time

websites = {}
appslist = {}

def deciding():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if "- Google" in GetWindowText(GetForegroundWindow()):
        websites[dt_string] = GetWindowText(GetForegroundWindow())
        url = 'http://www.x.com' #LOL
    else:
        appslist[dt_string] = GetWindowText(GetForegroundWindow())

def f(f_stop):
    # do something here ...
    deciding()
    #stuff.append(GetWindowText(GetForegroundWindow()))
    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(1, f, [f_stop]).start()

f_stop = threading.Event()
# start calling f now and every 60 sec thereafter
f(f_stop)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Rebecca'}
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if "- Google" in GetWindowText(GetForegroundWindow()):
        websites[dt_string] = GetWindowText(GetForegroundWindow())
    url = 'http://www.x.com' #lol later create a page that says, this is an application, there is no url loserrrr
    return render_template('index.html', title='Websites', user=user, websites=websites, url=url)

@app.route('/')
@app.route('/apps')
def apps():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if "- Google" not in GetWindowText(GetForegroundWindow()):
        appslist[dt_string] = GetWindowText(GetForegroundWindow())
    return render_template('apps.html', title='Apps', appslist=appslist)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

'''


'''
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
from win32gui import GetWindowText, GetForegroundWindow
import threading
from datetime import datetime
import uiautomation as auto
import socket
import pickle
import time
import pandas as pd

HEADERSIZE = 10

socketio = SocketIO(app)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1238))

websites = {}
appslist = {}

#removed all print statements lol
def deciding():
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(1024)
        if new_msg:
            #print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        #print(f"full message length: {msglen}")

        full_msg += msg

        #print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msglen:
            #print("full msg recvd")
            #print(full_msg[HEADERSIZE:])
            dfwebsites = pickle.loads(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = b""

def f(f_stop):
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(1024)
        if new_msg:
            #print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        #print(f"full message length: {msglen}")

        full_msg += msg

        #print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            #print(full_msg[HEADERSIZE:])
            dfwebsites = pickle.loads(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = b""
    if not f_stop.is_set():
        # call f() again in 60 seconds
        threading.Timer(1, f, [f_stop]).start()

f_stop = threading.Event()
# start calling f now and every 60 sec thereafter
f(f_stop)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Rebecca'}
    return render_template('index.html', title='Websites', dfwebsites=dfwebsites)

@app.route('/')
@app.route('/apps')
def apps():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if "- Google" not in GetWindowText(GetForegroundWindow()):
        appslist[dt_string] = GetWindowText(GetForegroundWindow())
    return render_template('apps.html', title='Apps', appslist=appslist)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,threaded=True)
''' 
