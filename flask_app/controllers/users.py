from datetime import date
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.message import Message
from flask import flash
from datetime import datetime
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from werkzeug.exceptions import HTTPException, NotFound
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# HTML Template to login or register
from flask_app.controllers.env import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('log-in.html')

@app.route('/signup')
def log():
    if 'user_id' in session:
        return redirect('/')
    return render_template('index.html')


#POST Method to create a User ex. Register

@app.route('/createUser', methods=['POST'])
def createUser():
    if not User.validate_user(request.form):
        flash('Somethings wrong ninja!', 'signUp')
        return redirect(request.referrer)
    
    if User.get_user_by_email(request.form):
        flash('This email already exists! What are you trying to do?!! Hack me?!', 'emailSignUp')
        return redirect(request.referrer)
    data = {
        'email': request.form['email'],
        'name': request.form['name'],
        'lastName': request.form['lastName'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'birthdate': request.form['birthdate']
    }
    User.create_user(data)
    return redirect('/')


#POST method to log the user in

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)
    if not User.get_user_by_email(data):
        flash('This email doesnt exist in this application', 'emailLogin')
        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
        
    session['user_id'] = user['id']
    return redirect('/')

# Route to display the main page 

@app.route('/')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        
        today = date.today()
        user = User.get_user_by_id(data)
        allEvents = Event.getAllEvents()
        userJoindEvents = User.get_logged_user_joind_events(data)
        count=0
        print("emriiiiiiii",allEvents)
        for event in allEvents:
            if (event['creator_id']== user['id']):

                if (today == event['date']):
                    count=count+1
        return render_template('dashboard.html', loggedUser= user, t=today, today=today.strftime("%B %d, %Y"),allEvents=allEvents, userJoindEvents=userJoindEvents, count=count,id=1 )
        #return render_template('dashboard.html', loggedUser= user, today=today.strftime("%B %d, %Y"))
    return redirect('/logout')


#Route to display a specific user information

@app.route('/profile')
def profileLogged():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        today = date.today()
        user = User.get_user_by_id(data)
        allEvents = Event.getAllEvents()
        userJoindEvents = User.get_logged_user_joind_events(data)
        return render_template('profile.html', user = user, today=today,allEvents=allEvents,userJoindEvents=userJoindEvents )
    return redirect('/logout')

@app.route('/user/<int:user_id>')
def profile(user_id):
    if 'user_id' in session:
        data = {
            'user_id': user_id
        }
        today = date.today()
        user = User.get_user_by_id(data)
        allEvents = Event.getAllEvents()
        userJoindEvents = User.get_logged_user_joind_events(data)
        return render_template('user_profile.html', user= user, today=today,allEvents=allEvents,userJoindEvents=userJoindEvents )
    return redirect('/logout')

#Route to log the user out -- Clean the session

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/loginPage')

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'user_id':id
    }
    user=User.get_user_by_id(data)
    return render_template('edit.html', user=user)

@app.route('/update/<int:id>', methods = ['POST'])
def updateUser(id):
    print (id)
    if 'user_id' not in session:
        return redirect('/logout')
    # if len(request.form['newpassword'])<1:
    #     data={
    #         'name': request.form['name'],
    #         'lastName': request.form['lastName'],
    #         'password': request.form['password']
    #     }
    data={
            'name': request.form['name'],
            'lastName': request.form['lastName'],
            'password': bcrypt.generate_password_hash(request.form['password']),
            'user_id': id
        }
    if not User.validate_edit_user(request.form):
        return redirect(request.referrer)

    if not session['user_id'] == id:
        return redirect('/dashboard')

    User.update_user(data)
    return redirect(request.referrer)


@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/uploadImage', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('Its required', 'file')
        return redirect(request.referrer)
    file = request.files['file']
    print(file)
    if file and allowed_file(file.filename):
        filename= secure_filename(file.filename)
        time = datetime.now().strftime("%d%m%Y%S%f")
        time += filename
        filename = time
        print (filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data={
            'photoName': filename,
            'user_id': session['user_id']
        }
        User.profilePic(data)
        return redirect('/profile') 
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect('/profile')

