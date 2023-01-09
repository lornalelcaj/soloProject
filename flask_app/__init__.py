from flask import Flask

import flask_app


app = Flask(__name__)
app.secret_key = 'My Secret Key! SHHHHH!'
