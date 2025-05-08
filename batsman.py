import google.generativeai as genai
import json
import re

def get_top_batsmen(selected_tournament):
    """
    Get top 5 batsmen from the selected tournament
    
    Args:
        selected_tournament (str): Name of the tournament to get stats for
        
    Returns:
        list: List of dictionaries containing batsman stats
    """
    # Set default year to 2023
    year = "2023"
    
    # Initialize Gemini client
    genai.configure(api_key="AIzaSyD-VS7-1R2YvrpoAAjP7SrA0tbJtaIwInA")
    
    # Generate prompt with default year
    prompt = f"""
    List me the top 5 batsmen of {selected_tournament} based on total runs scored in {year}.
    Provide the response in JSON format with the following structure:
    {{
        "tournament": "{selected_tournament}",
        "year": "{year}",
        "top_batsmen": [
            {{
                "rank": 1,
                "name": "Player Name",
                "runs": 999,
                "matches": 99,
                "average": 99.99,
                "highest_score": 999,
                "team": "Team Name"
            }},
            ... up to rank 5
        ]
    }}
    Include the team name for each player. Ensure to return valid JSON only. Do not include asterisks or any non-numeric characters in the highest_score field - it should be a number only.
    """
    
    # Get response from Gemini
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    
    # Get the response text
    response_text = response.text
    
    # Parse the response - handle various JSON formats that might be returned
    try:
        # Clean any asterisks from the JSON before parsing
        cleaned_text = clean_json_text(response_text)
        
        # Try to parse the entire response as JSON
        response_data = json.loads(cleaned_text)
        return response_data.get("top_batsmen", [])
    except json.JSONDecodeError:
        try:
            # Sometimes Gemini wraps JSON in markdown code blocks
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_text = response_text.split("```")[1].strip()
            else:
                # Try to find JSON block with starting/ending braces
                match = re.search(r'(\{.*\})', response_text, re.DOTALL)
                if match:
                    json_text = match.group(1)
                else:
                    raise ValueError("No valid JSON found in response")
            
            # Clean the JSON text to remove asterisks
            cleaned_json = clean_json_text(json_text)
            
            response_data = json.loads(cleaned_json)
            return response_data.get("top_batsmen", [])
        except (json.JSONDecodeError, ValueError, IndexError) as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response text: {response_text}")
            # Fallback to sample data if JSON parsing fails
            return get_fallback_batsman_data(selected_tournament)

def clean_json_text(json_text):
    """Clean JSON text to handle formatting issues from the API response."""
    # Fix the issue with asterisks in highest_score values like "220*"
    # Replace "220*" with 220 (remove the asterisk and keep the number)
    json_text = re.sub(r'(\d+)\*"', r'\1"', json_text)
    
    # Clean up any other potential JSON issues
    # Handle NaN, Infinity values which aren't valid in JSON
    json_text = json_text.replace('NaN', '"NaN"').replace('Infinity', '"Infinity"')
    
    return json_text

def get_fallback_batsman_data(tournament_name):
    """Return fallback data if API request fails"""
    # Sample data for different tournaments
    tournament_data = {
        'Ranji Trophy': [
            {
                "rank": 1,
                "name": "Mayank Agarwal",
                "runs": 990,
                "matches": 8,
                "average": 82.50,
                "highest_score": 249,
                "team": "Karnataka"
            },
            {
                "rank": 2,
                "name": "Ankit Bawne",
                "runs": 706,
                "matches": 7,
                "average": 58.83,
                "highest_score": 162,
                "team": "Maharashtra"
            },
            {
                "rank": 3,
                "name": "Riyan Parag",
                "runs": 699,
                "matches": 6,
                "average": 77.66,
                "highest_score": 155,
                "team": "Assam"
            },
            {
                "rank": 4,
                "name": "Shams Mulani",
                "runs": 614,
                "matches": 7,
                "average": 61.40,
                "highest_score": 145,
                "team": "Mumbai"
            },
            {
                "rank": 5,
                "name": "Sachin Baby",
                "runs": 610,
                "matches": 8,
                "average": 55.45,
                "highest_score": 142,
                "team": "Kerala"
            }
        ],
        'Irani Cup': [
            {
                "rank": 1,
                "name": "Abhimanyu Easwaran",
                "runs": 551,
                "matches": 6,
                "average": 61.22,
                "highest_score": 153,
                "team": "Rest of India"
            },
            {
                "rank": 2,
                "name": "Hanuma Vihari",
                "runs": 527,
                "matches": 5,
                "average": 58.55,
                "highest_score": 137,
                "team": "Rest of India"
            },
            {
                "rank": 3,
                "name": "Cheteshwar Pujara",
                "runs": 498,
                "matches": 5,
                "average": 55.33,
                "highest_score": 133,
                "team": "Saurashtra"
            },
            {
                "rank": 4,
                "name": "Sarfaraz Khan",
                "runs": 483,
                "matches": 5,
                "average": 60.38,
                "highest_score": 138,
                "team": "Rest of India"
            },
            {
                "rank": 5,
                "name": "Arpit Vasavada",
                "runs": 464,
                "matches": 5,
                "average": 51.56,
                "highest_score": 112,
                "team": "Saurashtra"
            }
        ],
        'Vijay Hazare Trophy': [
            {
                "rank": 1,
                "name": "Ruturaj Gaikwad",
                "runs": 660,
                "matches": 8,
                "average": 82.50,
                "highest_score": 220,
                "team": "Maharashtra"
            },
            {
                "rank": 2,
                "name": "Devdutt Padikkal",
                "runs": 609,
                "matches": 7,
                "average": 87.00,
                "highest_score": 145,
                "team": "Karnataka"
            },
            {
                "rank": 3,
                "name": "Prithvi Shaw",
                "runs": 595,
                "matches": 8,
                "average": 74.38,
                "highest_score": 185,
                "team": "Mumbai"
            },
            {
                "rank": 4,
                "name": "Narayan Jagadeesan",
                "runs": 585,
                "matches": 7,
                "average": 83.57,
                "highest_score": 168,
                "team": "Tamil Nadu"
            },
            {
                "rank": 5,
                "name": "Shreyas Iyer",
                "runs": 552,
                "matches": 7,
                "average": 79.00,
                "highest_score": 151,
                "team": "Mumbai"
            }
        ],
        'Syed Mushtaq Ali Trophy': [
            {
                "rank": 1,
                "name": "Abhishek Sharma",
                "runs": 485,
                "matches": 10,
                "average": 48.50,
                "highest_score": 104,
                "team": "Punjab"
            },
            {
                "rank": 2,
                "name": "Suryakumar Yadav",
                "runs": 480,
                "matches": 9,
                "average": 60.00,
                "highest_score": 117,
                "team": "Mumbai"
            },
            {
                "rank": 3,
                "name": "Riyan Parag",
                "runs": 462,
                "matches": 8,
                "average": 57.75,
                "highest_score": 112,
                "team": "Assam"
            },
            {
                "rank": 4,
                "name": "Ishan Kishan",
                "runs": 443,
                "matches": 9,
                "average": 49.22,
                "highest_score": 98,
                "team": "Jharkhand"
            },
            {
                "rank": 5,
                "name": "Tilak Varma",
                "runs": 429,
                "matches": 9,
                "average": 47.67,
                "highest_score": 93,
                "team": "Hyderabad"
            }
        ],
        'Duleep Trophy': [
            {
                "rank": 1,
                "name": "Ajinkya Rahane",
                "runs": 541,
                "matches": 5,
                "average": 60.11,
                "highest_score": 165,
                "team": "West Zone"
            },
            {
                "rank": 2,
                "name": "K.L. Rahul",
                "runs": 515,
                "matches": 5,
                "average": 57.22,
                "highest_score": 142,
                "team": "South Zone"
            },
            {
                "rank": 3,
                "name": "Mayank Agarwal",
                "runs": 483,
                "matches": 4,
                "average": 60.38,
                "highest_score": 153,
                "team": "South Zone"
            },
            {
                "rank": 4,
                "name": "Shreyas Iyer",
                "runs": 457,
                "matches": 5,
                "average": 50.78,
                "highest_score": 147,
                "team": "West Zone"
            },
            {
                "rank": 5,
                "name": "Abhimanyu Easwaran",
                "runs": 432,
                "matches": 4,
                "average": 54.00,
                "highest_score": 132,
                "team": "East Zone"
            }
        ],
        'Deodhar Trophy': [
            {
                "rank": 1,
                "name": "Ruturaj Gaikwad",
                "runs": 546,
                "matches": 6,
                "average": 78.00,
                "highest_score": 168,
                "team": "India C"
            },
            {
                "rank": 2,
                "name": "Shikhar Dhawan",
                "runs": 518,
                "matches": 6,
                "average": 64.75,
                "highest_score": 128,
                "team": "India A"
            },
            {
                "rank": 3,
                "name": "Prithvi Shaw",
                "runs": 501,
                "matches": 6,
                "average": 62.63,
                "highest_score": 145,
                "team": "India D"
            },
            {
                "rank": 4,
                "name": "Baba Indrajith",
                "runs": 476,
                "matches": 5,
                "average": 59.50,
                "highest_score": 127,
                "team": "India C"
            },
            {
                "rank": 5,
                "name": "Dhruv Shorey",
                "runs": 461,
                "matches": 6,
                "average": 57.63,
                "highest_score": 132,
                "team": "India B"
            }
        ]
    }
    
    # Return data for the requested tournament, or default to Ranji Trophy
    return tournament_data.get(tournament_name, tournament_data['Ranji Trophy'])

if __name__ == "__main__":
    # Available tournaments for testing
    tournaments = {
        '1': 'Ranji Trophy',
        '2': 'Irani Cup',
        '3': 'Vijay Hazare Trophy',
        '4': 'Syed Mushtaq Ali Trophy',
        '5': 'Duleep Trophy',
        '6': 'Deodhar Trophy'
    }
    
    # Display menu
    print("🏏 Select a Domestic Cricket Tournament in India:")
    for num, name in tournaments.items():
        print(f"{num}. {name}")
    
    # Get user input
    while True:
        choice = input("\nEnter your choice (1-6): ")
        if choice in tournaments:
            selected_tournament = tournaments[choice]
            break
        print("Invalid choice. Please enter a number between 1-6.")
    
    # Get and display batsman stats
    batsmen = get_top_batsmen(selected_tournament)
    print("\nTop Batsmen:")
    for batsman in batsmen:
        print(f"{batsman['rank']}. {batsman['name']} ({batsman['team']}) - {batsman['runs']} runs in {batsman['matches']} matches")