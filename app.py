# backend\app.py
from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import requests
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def get_posts():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        posts = response.json()
        return jsonify(posts)
    except Exception as e:
        print('Error fetching posts:', e)
        return jsonify(error='Failed to fetch posts'), 500

# Simulating new posts being created
def simulate_new_posts():
    while True:
        time.sleep(5)  # Simulate new posts every 5 seconds
        new_post = {'id': 101, 'title': 'New Post', 'body': 'This is a new post'}
        socketio.emit('new_post', new_post)

# Start the simulation in a separate thread
threading.Thread(target=simulate_new_posts, daemon=True).start()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
