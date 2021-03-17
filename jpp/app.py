import json
import os

from flask import Flask, render_template, request, send_from_directory
from flask_session import Session
from flask_socketio import SocketIO

app = Flask(__name__)
Session(app)
socketio = SocketIO(app, cors_allowed_origins='*')

def get_movie_data():
  with open(os.path.join(os.path.dirname(__file__), 'static', 'movies.json')) as f:
    return json.load(f)

@app.route('/')
def hello_world():
  movies = get_movie_data()['movies']
  return render_template('index.html', movies=movies)

# This is only used in development environments. In production, the /files/ path
# is statically mapped to nginx. See nginx.conf.
@app.route('/files/<path:filename>')
def files(filename):
  return send_from_directory('static/movies', filename)

@app.route('/movie/')
def movie():
  movies = get_movie_data()['movies']
  filename = request.args.get('filename')
  movie = list(filter(lambda m: m['filename'] == filename, movies))[0]
  return render_template('movie.html', movie=movie)

@app.route('/movie/play')
def start():
  socketio.emit('play')
  return ('', 204)

@app.route('/movie/pause')
def pause():
  socketio.emit('pause')
  return ('', 204)
