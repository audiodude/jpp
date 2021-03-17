import os

from bson.objectid import ObjectId
from flask import Flask, render_template, request
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
  return render_template('index.html', movies=movies)

@app.route('/movie/')
def movie():
  movie = db.movies.find_one({'_id': ObjectId(request.args.get('id'))})
  return render_template('movie.html', movie=movie)

@app.route('/movie/play')
def start():
  socketio.emit('play')
  return ('', 204)

@app.route('/movie/pause')
def pause():
  socketio.emit('pause')
  return ('', 204)