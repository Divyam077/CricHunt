from google import genai

def get_tournament_stats():
    # Available tournaments
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
    
    # Set default year to 2023
    year = "2023"
    
    # Initialize Gemini client
    client = genai.Client(api_key="AIzaSyB_W9t18sgLbGXoD_zeqPaLkF8oyPPO19g")
    
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
        ],
        "statistics_note": "Brief note about the tournament season"
    }}
    Include the team name for each player.
    """
    
    # Get response from Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    
    # Print and return the response
    print("\nTournament Statistics:")
    print(response.text)
    return response.text

if __name__ == "__main__":
    get_tournament_stats()