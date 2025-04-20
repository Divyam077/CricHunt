from flask import Flask, render_template, request, jsonify
import json
import os
from news import get_cricket_news
from bowler import get_top_bowlers
from batsman import get_top_batsmen

app = Flask(__name__)

# Define available tournaments
TOURNAMENTS = {
    '1': 'Ranji Trophy',
    '2': 'Irani Cup',
    '3': 'Vijay Hazare Trophy',
    '4': 'Syed Mushtaq Ali Trophy',
    '5': 'Duleep Trophy',
    '6': 'Deodhar Trophy'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', tournaments=TOURNAMENTS)

@app.route('/explore')
def explore():
    return render_template('explore.html', tournaments=TOURNAMENTS)

@app.route('/news')
def news():
    news_data = get_cricket_news()
    return render_template('news.html', news=news_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/get_tournament_stats', methods=['POST'])
def get_tournament_stats():
    data = request.json
    tournament_id = data.get('tournament_id')
    
    if tournament_id not in TOURNAMENTS:
        return jsonify({"error": "Invalid tournament ID"}), 400
    
    selected_tournament = TOURNAMENTS[tournament_id]
    
    # Get top bowlers and batsmen
    bowlers = get_top_bowlers(selected_tournament)
    batsmen = get_top_batsmen(selected_tournament)
    
    return jsonify({
        "tournament": selected_tournament,
        "bowlers": bowlers,
        "batsmen": batsmen
    })

if __name__ == '__main__':
    app.run(debug=True) 
