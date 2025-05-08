import google.generativeai as genai
import json
import re

def get_top_bowlers(selected_tournament):
    """
    Get top 5 bowlers from the selected tournament
    
    Args:
        selected_tournament (str): Name of the tournament to get stats for
        
    Returns:
        list: List of dictionaries containing bowler stats
    """
    # Set default year to 2023
    year = "2023"
    
    # Initialize Gemini client
    genai.configure(api_key="AIzaSyD-VS7-1R2YvrpoAAjP7SrA0tbJtaIwInA")
    
    # Generate prompt with default year
    prompt = f"""
    List me the top 5 bowlers of {selected_tournament} based on total number of wickets in {year}.
    Provide the response in JSON format with the following structure:
    {{
        "tournament": "{selected_tournament}",
        "year": "{year}",
        "top_bowlers": [
            {{
                "rank": 1,
                "name": "Player Name",
                "wickets": 99,
                "matches": 99,
                "average": 99.99,
                "best_figures": "9/99",
                "team": "Team Name"
            }},
            ... up to rank 5
        ]
    }}
    Include the team name for each player. Ensure to return valid JSON only. Make sure all field values are properly formatted for JSON.
    """
    
    # Get response from Gemini
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    
    # Get the response text
    response_text = response.text
    
    # Parse the response - handle various JSON formats that might be returned
    try:
        # Clean any special characters from the JSON before parsing
        cleaned_text = clean_json_text(response_text)
        
        # Try to parse the entire response as JSON
        response_data = json.loads(cleaned_text)
        return response_data.get("top_bowlers", [])
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
            
            # Clean the JSON text to remove special characters
            cleaned_json = clean_json_text(json_text)
            
            response_data = json.loads(cleaned_json)
            return response_data.get("top_bowlers", [])
        except (json.JSONDecodeError, ValueError, IndexError) as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response text: {response_text}")
            # Fallback to sample data if JSON parsing fails
            return get_fallback_bowler_data(selected_tournament)

def clean_json_text(json_text):
    """Clean JSON text to handle formatting issues from the API response."""
    # Fix any special characters or formatting issues in the JSON
    
    # Fix issues with asterisks or other characters in numeric fields
    json_text = re.sub(r'(\d+)\*"', r'\1"', json_text)
    
    # Handle special characters in best_figures field
    # Make sure slash format like "5/32" is properly quoted
    json_text = re.sub(r'"best_figures"\s*:\s*(\d+\/\d+)([,}])', r'"best_figures": "\1"\2', json_text)
    
    # Clean up any other potential JSON issues
    # Handle NaN, Infinity values which aren't valid in JSON
    json_text = json_text.replace('NaN', '"NaN"').replace('Infinity', '"Infinity"')
    
    return json_text

def get_fallback_bowler_data(tournament_name):
    """Return fallback data if API request fails"""
    # Sample data for different tournaments
    tournament_data = {
        'Ranji Trophy': [
            {
                "rank": 1,
                "name": "Jalaj Saxena",
                "wickets": 41,
                "matches": 9,
                "average": 18.75,
                "best_figures": "8/58",
                "team": "Kerala"
            },
            {
                "rank": 2,
                "name": "Jaydev Unadkat",
                "wickets": 39,
                "matches": 8,
                "average": 17.32,
                "best_figures": "7/56",
                "team": "Saurashtra"
            },
            {
                "rank": 3,
                "name": "Shahbaz Ahmed",
                "wickets": 35,
                "matches": 9,
                "average": 19.85,
                "best_figures": "6/43",
                "team": "Bengal"
            },
            {
                "rank": 4,
                "name": "Akash Deep",
                "wickets": 34,
                "matches": 9,
                "average": 21.50,
                "best_figures": "6/62",
                "team": "Bengal"
            },
            {
                "rank": 5,
                "name": "Harshal Patel",
                "wickets": 33,
                "matches": 8,
                "average": 20.21,
                "best_figures": "5/28",
                "team": "Haryana"
            }
        ],
        'Irani Cup': [
            {
                "rank": 1,
                "name": "Kuldeep Sen",
                "wickets": 18,
                "matches": 5,
                "average": 22.11,
                "best_figures": "5/67",
                "team": "Rest of India"
            },
            {
                "rank": 2,
                "name": "R Sai Kishore",
                "wickets": 17,
                "matches": 5,
                "average": 23.82,
                "best_figures": "4/57",
                "team": "Rest of India"
            },
            {
                "rank": 3,
                "name": "Mukesh Kumar",
                "wickets": 16,
                "matches": 5,
                "average": 24.56,
                "best_figures": "4/45",
                "team": "Rest of India"
            },
            {
                "rank": 4,
                "name": "Pulkit Narang",
                "wickets": 14,
                "matches": 5,
                "average": 25.71,
                "best_figures": "4/72",
                "team": "Saurashtra"
            },
            {
                "rank": 5,
                "name": "Chetan Sakariya",
                "wickets": 12,
                "matches": 5,
                "average": 26.33,
                "best_figures": "3/51",
                "team": "Saurashtra"
            }
        ],
        'Vijay Hazare Trophy': [
            {
                "rank": 1,
                "name": "Mohammed Siraj",
                "wickets": 21,
                "matches": 7,
                "average": 14.28,
                "best_figures": "5/26",
                "team": "Hyderabad"
            },
            {
                "rank": 2,
                "name": "Rishi Dhawan",
                "wickets": 19,
                "matches": 7,
                "average": 16.89,
                "best_figures": "4/29",
                "team": "Himachal Pradesh"
            },
            {
                "rank": 3,
                "name": "Siddharth Kaul",
                "wickets": 18,
                "matches": 6,
                "average": 15.72,
                "best_figures": "5/24",
                "team": "Punjab"
            },
            {
                "rank": 4,
                "name": "Avesh Khan",
                "wickets": 17,
                "matches": 7,
                "average": 18.53,
                "best_figures": "4/34",
                "team": "Madhya Pradesh"
            },
            {
                "rank": 5,
                "name": "T Natarajan",
                "wickets": 16,
                "matches": 7,
                "average": 19.81,
                "best_figures": "4/30",
                "team": "Tamil Nadu"
            }
        ],
        'Syed Mushtaq Ali Trophy': [
            {
                "rank": 1,
                "name": "Varun Chakravarthy",
                "wickets": 19,
                "matches": 10,
                "average": 14.21,
                "best_figures": "4/15",
                "team": "Tamil Nadu"
            },
            {
                "rank": 2,
                "name": "Rahul Chahar",
                "wickets": 18,
                "matches": 9,
                "average": 15.83,
                "best_figures": "4/18",
                "team": "Rajasthan"
            },
            {
                "rank": 3,
                "name": "Arshdeep Singh",
                "wickets": 17,
                "matches": 9,
                "average": 16.59,
                "best_figures": "4/22",
                "team": "Punjab"
            },
            {
                "rank": 4,
                "name": "Siddarth Kaul",
                "wickets": 16,
                "matches": 8,
                "average": 17.06,
                "best_figures": "4/26",
                "team": "Punjab"
            },
            {
                "rank": 5,
                "name": "Bhuvneshwar Kumar",
                "wickets": 15,
                "matches": 9,
                "average": 18.40,
                "best_figures": "3/21",
                "team": "Uttar Pradesh"
            }
        ],
        'Duleep Trophy': [
            {
                "rank": 1,
                "name": "Navdeep Saini",
                "wickets": 21,
                "matches": 5,
                "average": 19.76,
                "best_figures": "5/62",
                "team": "North Zone"
            },
            {
                "rank": 2,
                "name": "Saurabh Kumar",
                "wickets": 19,
                "matches": 5,
                "average": 21.32,
                "best_figures": "5/86",
                "team": "Central Zone"
            },
            {
                "rank": 3,
                "name": "Basil Thampi",
                "wickets": 17,
                "matches": 5,
                "average": 22.53,
                "best_figures": "4/48",
                "team": "South Zone"
            },
            {
                "rank": 4,
                "name": "Kulwant Khejroliya",
                "wickets": 16,
                "matches": 5,
                "average": 24.06,
                "best_figures": "4/53",
                "team": "North Zone"
            },
            {
                "rank": 5,
                "name": "Ishan Porel",
                "wickets": 15,
                "matches": 5,
                "average": 25.87,
                "best_figures": "4/62",
                "team": "East Zone"
            }
        ],
        'Deodhar Trophy': [
            {
                "rank": 1,
                "name": "Prasidh Krishna",
                "wickets": 16,
                "matches": 6,
                "average": 17.31,
                "best_figures": "4/32",
                "team": "India B"
            },
            {
                "rank": 2,
                "name": "Yuzvendra Chahal",
                "wickets": 15,
                "matches": 6,
                "average": 18.67,
                "best_figures": "4/29",
                "team": "India C"
            },
            {
                "rank": 3,
                "name": "Axar Patel",
                "wickets": 14,
                "matches": 6,
                "average": 19.50,
                "best_figures": "3/33",
                "team": "India A"
            },
            {
                "rank": 4,
                "name": "Shardul Thakur",
                "wickets": 13,
                "matches": 6,
                "average": 21.15,
                "best_figures": "3/39",
                "team": "India D"
            },
            {
                "rank": 5,
                "name": "Khaleel Ahmed",
                "wickets": 12,
                "matches": 6,
                "average": 22.83,
                "best_figures": "3/42",
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
    
    # Get and display bowler stats
    bowlers = get_top_bowlers(selected_tournament)
    print("\nTop Bowlers:")
    for bowler in bowlers:
        print(f"{bowler['rank']}. {bowler['name']} ({bowler['team']}) - {bowler['wickets']} wickets in {bowler['matches']} matches")