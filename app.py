from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import jwt
import datetime
import json
import os
from functools import wraps

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
SECRET_KEY = "your_secret_key"  # Use env var in production

# Load roadmap data
ROADMAP_PATH = os.path.join(os.path.dirname(__file__), 'roadmap_data', 'roadmaps.json')
with open(ROADMAP_PATH, 'r', encoding='utf-8') as f:
    ROADMAPS = json.load(f)

# User store
USERS_PATH = os.path.join(os.path.dirname(__file__), 'users.json')
if not os.path.exists(USERS_PATH):
    with open(USERS_PATH, 'w') as f:
        json.dump({}, f)

def load_users():
    with open(USERS_PATH, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_PATH, 'w') as f:
        json.dump(users, f)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['username']
        except Exception as e:
            return jsonify({'error': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    users = load_users()
    if username in users:
        return jsonify({'error': 'User already exists'}), 400
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    users[username] = {'password': pw_hash}
    save_users(users)
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    users = load_users()
    user = users.get(username)
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token})

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Hello, {current_user}! This is a protected route.'})

@app.route('/suggest', methods=['POST'])
@token_required
def suggest_tracks(current_user):
    data = request.json
    interests = data.get('interests', [])
    time_commitment = data.get('time_commitment', '')
    goals = data.get('goals', [])

    suggestions = []
    if 'coding' in interests:
        suggestions += ["Web Developer", "Python Backend Developer", "Mobile Developer (Flutter/React Native)", "Data Analyst", "AI/ML Enthusiast", "DevOps Engineer"]
    if 'design' in interests:
        suggestions += ["UI/UX Designer"]
    if 'entrepreneurship' in interests:
        suggestions += ["Shopify Expert", "Digital Marketer"]
    if 'management' in interests:
        suggestions += ["Product Manager", "Tech Recruiter"]
    if 'writing' in interests:
        suggestions += ["Copywriter"]
    seen = set()
    suggestions = [x for x in suggestions if not (x in seen or seen.add(x))]
    if not suggestions:
        suggestions = list(ROADMAPS.keys())[:5]
    return jsonify({"suggestions": suggestions})

@app.route('/roadmap/<track>', methods=['GET'])
@token_required
def get_roadmap(current_user, track):
    track = track.replace('-', ' ')
    roadmap = ROADMAPS.get(track)
    if not roadmap:
        return jsonify({"error": "Roadmap not found"}), 404
    return jsonify(roadmap)

@app.route('/ai-counselor', methods=['POST'])
@token_required
def ai_counselor(current_user):
    data = request.json
    user_query = data.get('query', '')
    response = "AI Counselor is coming soon! For now, try focusing on coding paths that require less math, like web development or UI/UX."
    return jsonify({"advice": response})

if __name__ == '__main__':
    app.run(debug=True) 