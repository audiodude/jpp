import os

from flask import Flask, render_template
from flask_session import Session
from flask_socketio import SocketIO
from pymongo import MongoClient

app = Flask(__name__)
Session(app)
socketio = SocketIO(app, cors_allowed_origins='*')

MONGO_URL = os.environ.get('MONGO_URL') or 'mongodb://localhost:27017'
client = MongoClient(MONGO_URL,
                     connectTimeoutMS=2000,
                     serverSelectionTimeoutMS=6000)
db = client.jpp

@app.route('/')
def hello_world():
  movies = list(db.movies.find())
  return render_template('index.html.jinja2', movies=movies)