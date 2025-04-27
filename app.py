from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
import base64
import cv2
import numpy as np
from gesture_service import GestureService
from collections import deque
import mediapipe as mp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

gesture_service = GestureService()
point_history = deque(maxlen=16)

# Load or create users.json
USER_FILE = 'users.json'
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('smart_home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = load_users()
        if username in users:
            flash('Username already exists. Try logging in.', 'warning')
        else:
            users[username] = password
            save_users(users)
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')   
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 403

    try:
        # Decode the image from base64
        data_url = request.json['image']
        _, encoded = data_url.split(",", 1)
        image_data = base64.b64decode(encoded)
        np_arr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Run Mediapipe detection
        with mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7) as hands:
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = [[lm.x, lm.y] for lm in hand_landmarks.landmark]

                    # Static gesture
                    static_label = gesture_service.classify_static(landmarks)

                    # Dynamic gesture (if point history ready)
                    index_finger_tip = landmarks[8] if len(landmarks) > 8 else [0, 0]
                    point_history.append(index_finger_tip)

                    if len(point_history) == point_history.maxlen:
                        dynamic_label = gesture_service.classify_dynamic(list(point_history))
                        return jsonify({'label': dynamic_label})
                    else:
                        return jsonify({'label': static_label})

            return jsonify({'label': 'No hand detected'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/smart_home')
def smart_home():
    print("Accessing /smart_home route")
    if 'username' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('smart_home.html')

@app.route('/contact')
def contact():
    if 'username' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
