from flask import Flask, render_template, request, jsonify
import json
import os
from news import get_cricket_news
from bowler import get_top_bowlers
from batsman import get_top_batsmen
import requests
import time

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

# Define tournament data
TOURNAMENT_DATA = {
    '1': {  # Ranji Trophy
        'bowlers': [
            {'rank': 1, 'name': 'Ravichandran Ashwin', 'team': 'Tamil Nadu', 'wickets': 67, 'matches': 7, 'average': 15.89, 'best_figures': '7/56'},
            {'rank': 2, 'name': 'Shahbaz Nadeem', 'team': 'Jharkhand', 'wickets': 51, 'matches': 6, 'average': 19.23, 'best_figures': '6/18'},
            {'rank': 3, 'name': 'Jaydev Unadkat', 'team': 'Saurashtra', 'wickets': 49, 'matches': 6, 'average': 20.12, 'best_figures': '6/85'},
            {'rank': 4, 'name': 'Rahul Chahar', 'team': 'Rajasthan', 'wickets': 45, 'matches': 6, 'average': 22.33, 'best_figures': '5/45'},
            {'rank': 5, 'name': 'Saurabh Kumar', 'team': 'Uttar Pradesh', 'wickets': 43, 'matches': 6, 'average': 23.45, 'best_figures': '5/33'}
        ],
        'batsmen': [
            {'rank': 1, 'name': 'Mayank Agarwal', 'team': 'Karnataka', 'runs': 990, 'matches': 6, 'average': 82.50, 'highest_score': '249'},
            {'rank': 2, 'name': 'Cheteshwar Pujara', 'team': 'Saurashtra', 'runs': 875, 'matches': 6, 'average': 79.54, 'highest_score': '248'},
            {'rank': 3, 'name': 'Shubman Gill', 'team': 'Punjab', 'runs': 728, 'matches': 5, 'average': 104.00, 'highest_score': '268'},
            {'rank': 4, 'name': 'Abhimanyu Easwaran', 'team': 'Bengal', 'runs': 698, 'matches': 6, 'average': 69.80, 'highest_score': '201'},
            {'rank': 5, 'name': 'Ruturaj Gaikwad', 'team': 'Maharashtra', 'runs': 660, 'matches': 6, 'average': 73.33, 'highest_score': '220'}
        ]
    },
    '2': {  # Irani Cup
        'bowlers': [
            {'rank': 1, 'name': 'Jaydev Unadkat', 'team': 'Rest of India', 'wickets': 8, 'matches': 1, 'average': 15.25, 'best_figures': '4/61'},
            {'rank': 2, 'name': 'Ravichandran Ashwin', 'team': 'Rest of India', 'wickets': 6, 'matches': 1, 'average': 18.33, 'best_figures': '3/55'},
            {'rank': 3, 'name': 'Saurabh Kumar', 'team': 'Rest of India', 'wickets': 5, 'matches': 1, 'average': 20.40, 'best_figures': '3/102'},
            {'rank': 4, 'name': 'Rahul Chahar', 'team': 'Rest of India', 'wickets': 4, 'matches': 1, 'average': 22.50, 'best_figures': '2/45'},
            {'rank': 5, 'name': 'Navdeep Saini', 'team': 'Rest of India', 'wickets': 3, 'matches': 1, 'average': 25.33, 'best_figures': '2/76'}
        ],
        'batsmen': [
            {'rank': 1, 'name': 'Yashasvi Jaiswal', 'team': 'Rest of India', 'runs': 213, 'matches': 1, 'average': 106.50, 'highest_score': '144'},
            {'rank': 2, 'name': 'Hanuma Vihari', 'team': 'Rest of India', 'runs': 180, 'matches': 1, 'average': 90.00, 'highest_score': '180'},
            {'rank': 3, 'name': 'Abhimanyu Easwaran', 'team': 'Rest of India', 'runs': 154, 'matches': 1, 'average': 77.00, 'highest_score': '154'},
            {'rank': 4, 'name': 'Ruturaj Gaikwad', 'team': 'Rest of India', 'runs': 108, 'matches': 1, 'average': 54.00, 'highest_score': '108'},
            {'rank': 5, 'name': 'Sarfaraz Khan', 'team': 'Rest of India', 'runs': 95, 'matches': 1, 'average': 47.50, 'highest_score': '95'}
        ]
    },
    '3': {  # Vijay Hazare Trophy
        'bowlers': [
            {'rank': 1, 'name': 'Yuzvendra Chahal', 'team': 'Haryana', 'wickets': 22, 'matches': 7, 'average': 12.68, 'best_figures': '5/31'},
            {'rank': 2, 'name': 'Ravi Bishnoi', 'team': 'Rajasthan', 'wickets': 18, 'matches': 6, 'average': 15.22, 'best_figures': '4/28'},
            {'rank': 3, 'name': 'Shahbaz Ahmed', 'team': 'Bengal', 'wickets': 16, 'matches': 6, 'average': 16.75, 'best_figures': '4/22'},
            {'rank': 4, 'name': 'Rahul Chahar', 'team': 'Rajasthan', 'wickets': 15, 'matches': 6, 'average': 18.20, 'best_figures': '3/25'},
            {'rank': 5, 'name': 'Kuldeep Yadav', 'team': 'Uttar Pradesh', 'wickets': 14, 'matches': 5, 'average': 19.14, 'best_figures': '3/30'}
        ],
        'batsmen': [
            {'rank': 1, 'name': 'Ruturaj Gaikwad', 'team': 'Maharashtra', 'runs': 660, 'matches': 5, 'average': 132.00, 'highest_score': '220'},
            {'rank': 2, 'name': 'Shubman Gill', 'team': 'Punjab', 'runs': 580, 'matches': 5, 'average': 116.00, 'highest_score': '187'},
            {'rank': 3, 'name': 'Ishan Kishan', 'team': 'Jharkhand', 'runs': 540, 'matches': 5, 'average': 108.00, 'highest_score': '173'},
            {'rank': 4, 'name': 'Devdutt Padikkal', 'team': 'Karnataka', 'runs': 520, 'matches': 5, 'average': 104.00, 'highest_score': '152'},
            {'rank': 5, 'name': 'Prithvi Shaw', 'team': 'Mumbai', 'runs': 490, 'matches': 5, 'average': 98.00, 'highest_score': '185'}
        ]
    },
    '4': {  # Syed Mushtaq Ali Trophy
        'bowlers': [
            {'rank': 1, 'name': 'Ravi Bishnoi', 'team': 'Rajasthan', 'wickets': 18, 'matches': 6, 'average': 12.33, 'best_figures': '4/15'},
            {'rank': 2, 'name': 'Yuzvendra Chahal', 'team': 'Haryana', 'wickets': 16, 'matches': 5, 'average': 13.75, 'best_figures': '3/20'},
            {'rank': 3, 'name': 'Rahul Chahar', 'team': 'Rajasthan', 'wickets': 15, 'matches': 6, 'average': 14.20, 'best_figures': '3/18'},
            {'rank': 4, 'name': 'Arshdeep Singh', 'team': 'Punjab', 'wickets': 14, 'matches': 5, 'average': 15.14, 'best_figures': '3/22'},
            {'rank': 5, 'name': 'Mohammed Siraj', 'team': 'Hyderabad', 'wickets': 13, 'matches': 5, 'average': 16.15, 'best_figures': '3/25'}
        ],
        'batsmen': [
            {'rank': 1, 'name': 'Ruturaj Gaikwad', 'team': 'Maharashtra', 'runs': 420, 'matches': 5, 'average': 105.00, 'highest_score': '112'},
            {'rank': 2, 'name': 'Prithvi Shaw', 'team': 'Mumbai', 'runs': 380, 'matches': 5, 'average': 95.00, 'highest_score': '134'},
            {'rank': 3, 'name': 'Ishan Kishan', 'team': 'Jharkhand', 'runs': 360, 'matches': 5, 'average': 90.00, 'highest_score': '113'},
            {'rank': 4, 'name': 'Devdutt Padikkal', 'team': 'Karnataka', 'runs': 340, 'matches': 5, 'average': 85.00, 'highest_score': '124'},
            {'rank': 5, 'name': 'Shubman Gill', 'team': 'Punjab', 'runs': 320, 'matches': 5, 'average': 80.00, 'highest_score': '126'}
        ]
    },
    '5': {  # Duleep Trophy
        'bowlers': [
            {'rank': 1, 'name': 'Jaydev Unadkat', 'team': 'West Zone', 'wickets': 12, 'matches': 2, 'average': 16.25, 'best_figures': '5/45'},
            {'rank': 2, 'name': 'Ravichandran Ashwin', 'team': 'South Zone', 'wickets': 10, 'matches': 2, 'average': 18.30, 'best_figures': '4/52'},
            {'rank': 3, 'name': 'Saurabh Kumar', 'team': 'North Zone', 'wickets': 9, 'matches': 2, 'average': 19.44, 'best_figures': '4/48'},
            {'rank': 4, 'name': 'Rahul Chahar', 'team': 'West Zone', 'wickets': 8, 'matches': 2, 'average': 20.50, 'best_figures': '3/42'},
            {'rank': 5, 'name': 'Navdeep Saini', 'team': 'North Zone', 'wickets': 7, 'matches': 2, 'average': 21.71, 'best_figures': '3/55'}
        ],
        'batsmen': [
            {'rank': 1, 'name': 'Yashasvi Jaiswal', 'team': 'West Zone', 'runs': 265, 'matches': 2, 'average': 88.33, 'highest_score': '145'},
            {'rank': 2, 'name': 'Hanuma Vihari', 'team': 'South Zone', 'runs': 240, 'matches': 2, 'average': 80.00, 'highest_score': '138'},
            {'rank': 3, 'name': 'Abhimanyu Easwaran', 'team': 'East Zone', 'runs': 220, 'matches': 2, 'average': 73.33, 'highest_score': '128'},
            {'rank': 4, 'name': 'Ruturaj Gaikwad', 'team': 'West Zone', 'runs': 210, 'matches': 2, 'average': 70.00, 'highest_score': '118'},
            {'rank': 5, 'name': 'Sarfaraz Khan', 'team': 'West Zone', 'runs': 195, 'matches': 2, 'average': 65.00, 'highest_score': '125'}
        ]
    },
    '6': {  # Deodhar Trophy
        'bowlers': [
            {'rank': 1, 'name': 'Ravi Bishnoi', 'team': 'India B', 'wickets': 10, 'matches': 3, 'average': 14.20, 'best_figures': '4/25'},
            {'rank': 2, 'name': 'Yuzvendra Chahal', 'team': 'India A', 'wickets': 9, 'matches': 3, 'average': 15.33, 'best_figures': '3/28'},
            {'rank': 3, 'name': 'Rahul Chahar', 'team': 'India C', 'wickets': 8, 'matches': 3, 'average': 16.50, 'best_figures': '3/30'},
            {'rank': 4, 'name': 'Shahbaz Ahmed', 'team': 'India B', 'wickets': 7, 'matches': 3, 'average': 17.71, 'best_figures': '3/32'},
            {'rank': 5, 'name': 'Kuldeep Yadav', 'team': 'India A', 'wickets': 6, 'matches': 3, 'average': 18.83, 'best_figures': '3/35'}
        ],
        'batsmen': [
            {'rank': 1, 'name': 'Ruturaj Gaikwad', 'team': 'India A', 'runs': 280, 'matches': 3, 'average': 93.33, 'highest_score': '132'},
            {'rank': 2, 'name': 'Shubman Gill', 'team': 'India B', 'runs': 260, 'matches': 3, 'average': 86.66, 'highest_score': '128'},
            {'rank': 3, 'name': 'Ishan Kishan', 'team': 'India C', 'runs': 240, 'matches': 3, 'average': 80.00, 'highest_score': '118'},
            {'rank': 4, 'name': 'Devdutt Padikkal', 'team': 'India A', 'runs': 220, 'matches': 3, 'average': 73.33, 'highest_score': '112'},
            {'rank': 5, 'name': 'Prithvi Shaw', 'team': 'India B', 'runs': 200, 'matches': 3, 'average': 66.66, 'highest_score': '108'}
        ]
    }
}

# Gemini API credentials
GEMINI_API_KEY = "AIzaSyAv5PecntZP_pCDXjEA40Q2FUOHHZeaDUE"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def make_gemini_request(prompt, max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers={'Content-Type': 'application/json'},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }]
                }
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                if attempt < max_retries - 1:  # If we haven't tried all retries yet
                    print(f"API overloaded, retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    continue
                else:
                    print("Max retries reached, API still overloaded")
                    return None
            else:
                print(f"API Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"Request error: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return None
    
    return None

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

@app.route('/player-search')
def player_search():
    return render_template('player_search.html')

@app.route('/player-comparison')
def player_comparison():
    return render_template('player_comparison.html')

@app.route('/api/search-player', methods=['POST'])
def search_player():
    player_name = request.json.get('player_name')
    if not player_name:
        return jsonify({"error": "Player name is required"}), 400
    
    try:
        # Use a simpler prompt to reduce API load
        prompt = f"""Provide a brief summary about the cricket player {player_name}. Include:
        - Role (batsman/bowler/all-rounder)
        - Test batting average
        - ODI batting average
        - Centuries
        - Test wickets
        - ODI wickets
        - Key achievements
        Keep the response concise and informative."""

        # Make request to Gemini API with retry logic
        data = make_gemini_request(prompt)
        
        if data is None:
            # Fallback to a simpler response if API is unavailable
            return jsonify({
                "results": [{
                    "title": f"About {player_name}",
                    "snippet": "Service temporarily unavailable. Please try again later.",
                    "link": f"https://en.wikipedia.org/wiki/{player_name.replace(' ', '_')}"
                }]
            })
        
        try:
            generated_text = data['candidates'][0]['content']['parts'][0]['text']
            
            # Format the response
            result = {
                "title": f"About {player_name}",
                "snippet": generated_text,
                "link": f"https://en.wikipedia.org/wiki/{player_name.replace(' ', '_')}"
            }
            
            return jsonify({
                "results": [result]
            })
        except (KeyError, IndexError) as e:
            print("Error extracting text:", e)
            # Return a structured error response
            return jsonify({
                "results": [{
                    "title": f"About {player_name}",
                    "snippet": "Failed to retrieve player information. Please try again.",
                    "link": f"https://en.wikipedia.org/wiki/{player_name.replace(' ', '_')}"
                }]
            })
            
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({
            "results": [{
                "title": f"About {player_name}",
                "snippet": f"An error occurred: {str(e)}",
                "link": f"https://en.wikipedia.org/wiki/{player_name.replace(' ', '_')}"
            }]
        })

@app.route('/api/compare-players', methods=['POST'])
def compare_players():
    data = request.json
    player1 = data.get('player1')
    player2 = data.get('player2')
    
    if not player1 or not player2:
        return jsonify({"error": "Both player names are required"}), 400
    
    try:
        # Use a simpler prompt to reduce API load
        prompt = f"""Compare {player1} and {player2} in cricket. Provide their statistics in the following format:
        For {player1}:
        Role: [role]
        Test Average: [number]
        ODI Average: [number]
        Test Centuries: [number]
        ODI Centuries: [number]
        Test Wickets: [number]
        ODI Wickets: [number]
        Key Achievements: [text]

        For {player2}:
        Role: [role]
        Test Average: [number]
        ODI Average: [number]
        Test Centuries: [number]
        ODI Centuries: [number]
        Test Wickets: [number]
        ODI Wickets: [number]
        Key Achievements: [text]"""

        # Make request to Gemini API with retry logic
        response_data = make_gemini_request(prompt)
        
        if response_data is None:
            # Fallback to a simpler comparison if API is unavailable
            return jsonify({
                "player1": {
                    "name": player1,
                    "stats": {
                        "Role": "Information unavailable",
                        "Test Average": "N/A",
                        "ODI Average": "N/A",
                        "Test Centuries": "N/A",
                        "ODI Centuries": "N/A",
                        "Test Wickets": "N/A",
                        "ODI Wickets": "N/A",
                        "Key Achievements": "Service temporarily unavailable. Please try again later."
                    }
                },
                "player2": {
                    "name": player2,
                    "stats": {
                        "Role": "Information unavailable",
                        "Test Average": "N/A",
                        "ODI Average": "N/A",
                        "Test Centuries": "N/A",
                        "ODI Centuries": "N/A",
                        "Test Wickets": "N/A",
                        "ODI Wickets": "N/A",
                        "Key Achievements": "Service temporarily unavailable. Please try again later."
                    }
                }
            })
        
        try:
            generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
            
            # Parse the generated text into structured data
            lines = generated_text.split('\n')
            current_player = None
            player1_stats = {}
            player2_stats = {}
            current_stats = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if f"For {player1}:" in line:
                    current_player = "player1"
                    current_stats = player1_stats
                    continue
                elif f"For {player2}:" in line:
                    current_player = "player2"
                    current_stats = player2_stats
                    continue
                
                if current_stats is not None and ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Convert numeric values to numbers
                    if value.replace('.', '').isdigit():
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    
                    current_stats[key] = value
            
            # Ensure all required stats are present
            required_stats = ['Role', 'Test Average', 'ODI Average', 'Test Centuries', 
                            'ODI Centuries', 'Test Wickets', 'ODI Wickets', 'Key Achievements']
            
            for stats in [player1_stats, player2_stats]:
                for stat in required_stats:
                    if stat not in stats:
                        stats[stat] = "N/A"
            
            comparison_data = {
                "player1": {
                    "name": player1,
                    "stats": player1_stats
                },
                "player2": {
                    "name": player2,
                    "stats": player2_stats
                }
            }
            
            return jsonify(comparison_data)
            
        except (KeyError, IndexError) as e:
            print("Error parsing response:", e)
            return jsonify({
                "error": "Failed to parse player data. Please try again."
            }), 500
            
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500

@app.route('/api/get_tournament_stats', methods=['POST'])
def get_tournament_stats():
    data = request.json
    tournament_id = data.get('tournament_id')
    
    if tournament_id not in TOURNAMENTS:
        return jsonify({"error": "Invalid tournament ID"}), 400
    
    selected_tournament = TOURNAMENTS[tournament_id]
    
    # Get manual data for the selected tournament
    tournament_data = TOURNAMENT_DATA.get(tournament_id, {
        'bowlers': [],
        'batsmen': []
    })
    
    return jsonify({
        "tournament": selected_tournament,
        "bowlers": tournament_data['bowlers'],
        "batsmen": tournament_data['batsmen']
    })

if __name__ == '__main__':
    app.run(debug=True) 