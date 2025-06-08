import json
import random
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

# Questions about Manuel Neuer
QUESTIONS = [
    {
        "question": "What position does Manuel Neuer play?",
        "options": ["Defender", "Goalkeeper", "Midfielder", "Forward"],
        "answer": 1
    },
    {
        "question": "Which club did Neuer join in 2011?",
        "options": ["Borussia Dortmund", "Bayern Munich", "Schalke 04", "Manchester City"],
        "answer": 1
    },
    {
        "question": "In which year was Neuer born?",
        "options": ["1984", "1986", "1988", "1990"],
        "answer": 1
    },
    {
        "question": "For which national team does Neuer play?",
        "options": ["Spain", "Germany", "France", "Italy"],
        "answer": 1
    },
    {
        "question": "How many FIFA World Cups has Neuer won?",
        "options": ["1", "2", "3", "0"],
        "answer": 0
    },
    {
        "question": "Which award did Neuer win in 2014 for best goalkeeper?",
        "options": ["Golden Glove", "Ballon d'Or", "Golden Boot", "Golden Ball"],
        "answer": 0
    },
    {
        "question": "What is Neuer known for besides shot-stopping?",
        "options": ["Dribbling", "Sweeper-keeper style", "Goal scoring", "Tackling"],
        "answer": 1
    },
    {
        "question": "Which youth club did Neuer start with?",
        "options": ["Bayern Munich", "Schalke 04", "Hamburger SV", "Werder Bremen"],
        "answer": 1
    },
    {
        "question": "How tall is Manuel Neuer?",
        "options": ["1.85m", "1.90m", "1.93m", "2.00m"],
        "answer": 2
    },
    {
        "question": "What number does Neuer typically wear for Bayern Munich?",
        "options": ["1", "10", "20", "5"],
        "answer": 0
    },
    {
        "question": "Which Champions League title was Neuer's first?",
        "options": ["2010", "2013", "2015", "2020"],
        "answer": 1
    },
    {
        "question": "Neuer's playing style is often compared to which famous keeper?",
        "options": ["Gianluigi Buffon", "Lev Yashin", "Iker Casillas", "Edwin van der Sar"],
        "answer": 1
    },
    {
        "question": "Where was Neuer born?",
        "options": ["Berlin", "Munich", "Gelsenkirchen", "Hamburg"],
        "answer": 2
    },
    {
        "question": "Which international tournament did Neuer captain Germany to win in 2014?",
        "options": ["EURO 2012", "World Cup 2014", "Confederations Cup 2017", "EURO 2016"],
        "answer": 1
    },
    {
        "question": "What is Neuer's nickname?",
        "options": ["Der Titan", "Sweeper King", "The Wall", "Manu"],
        "answer": 3
    }
]

LEADERBOARD_FILE = 'leaderboard.json'


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(data, f)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)


@app.route('/questions')
def get_questions():
    return jsonify(random.sample(QUESTIONS, 10))


@app.route('/submit', methods=['POST'])
def submit_score():
    data = request.get_json()
    username = data.get('username')
    score = data.get('score')

    leaderboard = load_leaderboard()
    # Update best score per user
    existing = next((item for item in leaderboard if item['username'] == username), None)
    if existing:
        if score > existing['score']:
            existing['score'] = score
    else:
        leaderboard.append({'username': username, 'score': score})

    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    save_leaderboard(leaderboard)
    return jsonify(leaderboard)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
