from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.event import Event
from flask_app.models.user import User
from flask_app.models.message import Message
from flask import  url_for
from datetime import date

@app.route('/createEvent', methods=['POST'])
def createEvent():

    if not Event.validate_event(request.form):
        return redirect(request.referrer)
    data = {
        'user_id': session['user_id'],
        'name' : request.form['name'],
        'location' : request.form['location'],
        'date': request.form['date'],
        'time': request.form['time'],
        'information': request.form['information'],
        'playerNr': request.form ['playerNr'],
        'type': request.form['type']
    }
    
    user=session['user_id']
    Event.create_event(data)
    # events=Event.get_event_by_userid(user)
    # userJoinedEvents=User.get_logged_user_joind_events(user)
    # print (events)
    # for i['id'] in events:
    #     if i['id'] not in userJoinedEvents:
    #         data1={
    #             'user_id' :session['user_id'],
    #             'event_id': i['id']
    #         }
    #         Event.addJoin(data1)
    return redirect('/')

@app.route('/create')
def create():

    return render_template('event.html')

@app.route('/search')
def search():

    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            'user_id': session['user_id']
        }
    today=date.today()
    showEvent=Event.getAllEvents()
    userJoindEvents = User.get_logged_user_joind_events(data)
    user=session['user_id']
    return render_template ('search.html',showEvent=showEvent,today=today, user=user,userJoindEvents=userJoindEvents, loggeduser=data['user_id'],searchedEvents=0)

# @app.route('/searchEvent', methods=['POST'])
# def Search():
#     data = {
#         'category': request.form['category'],
#         'name' : request.form['name']
#     }
#     showEvent=Event.search(data)
#     return redirect(url_for('rederector', showEvent=showEvent))
    
# @app.route('/rederector/<showEvent>')
# def displaySearch(showEvent):
#      return render_template('displaySearch.html',showEvent=showEvent )

@app.route('/event/<int:id>')
def event(id):
    if 'user_id' in session:
        data = {
            'event_id': id
        }
        data1 = {
            'user_id': session['user_id']
        }
    
        userJoindEvents = User.get_logged_user_joind_events(data1)

        event = Event.get_event_by_id(data)
        messages=Message.getAllMessages()
        users=Event.get_event_joind_users(data)
        print(users)
        return render_template('infoEvent.html', event= event, messages=messages, data=data, users=users, userJoindEvents=userJoindEvents)
    return redirect('/logout')

@app.route('/attend/<int:event_id>')
def join(event_id):
    if 'user_id' in session:
        data = {
            'event_id': event_id,
            'user_id': session['user_id']
        }
        Event.addJoin(data)
        return redirect(request.referrer)

        
@app.route('/unattend/<int:event_id>')
def unjoin(event_id):
    if 'user_id' in session:
        data = {
            'event_id': event_id,
            'user_id': session['user_id']
        }
        Event.removeJoin(data)
        return redirect(request.referrer)