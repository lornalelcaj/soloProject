from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.event import Event
from flask_app.models.user import User
from flask_app.models.message import Message

@app.route('/createMessage/<int:event_id>', methods=['POST'])
def createMessage(event_id):
    print(event_id)
    if 'user_id' not in session:
        return redirect('/logout')
    if not Message.validate_message(request.form):
        return redirect(request.referrer)
    data = {
        'user_id': session['user_id'],
        'event_id' : event_id,
        'content' : request.form['content']
    }
    Message.create_message(data)
    return redirect(request.referrer)
