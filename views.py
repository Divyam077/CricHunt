import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Player, Team, Tournament, Match, PlayerStats
from django.db.models import Q, F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce
import os

def get_tournament_data():
    file_path = os.path.join(os.path.dirname(__file__), 'info.txt')
    with open(file_path, 'r') as file:
        return json.load(file)

def home(request):
    return render(request, 'crichunt/home.html')

def search_players(request):
    query = request.GET.get('query', '')
    if query:
        players = Player.objects.filter(
            Q(name__icontains=query) |
            Q(team__name__icontains=query)
        ).select_related('team')[:10]
        results = [{
            'id': player.id,
            'name': player.name,
            'team': player.team.name if player.team else 'N/A',
            'role': player.role
        } for player in players]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

def player_comparison(request):
    player1_id = request.GET.get('player1')
    player2_id = request.GET.get('player2')
    
    if not player1_id or not player2_id:
        return JsonResponse({'error': 'Both players are required'}, status=400)
    
    try:
        player1 = Player.objects.get(id=player1_id)
        player2 = Player.objects.get(id=player2_id)
        
        # Get tournament data
        tournament_data = get_tournament_data()
        
        # Get player stats
        player1_stats = PlayerStats.objects.filter(player=player1).first()
        player2_stats = PlayerStats.objects.filter(player=player2).first()
        
        # Get tournament-specific data
        tournament_id = request.GET.get('tournament', '1')
        tournament_info = tournament_data.get(tournament_id, {})
        
        # Find players in tournament data
        player1_tournament = None
        player2_tournament = None
        
        for bowler in tournament_info.get('bowlers', []):
            if bowler['name'] == player1.name:
                player1_tournament = bowler
            if bowler['name'] == player2.name:
                player2_tournament = bowler
                
        for batsman in tournament_info.get('batsmen', []):
            if batsman['name'] == player1.name:
                player1_tournament = batsman
            if batsman['name'] == player2.name:
                player2_tournament = batsman
        
        response_data = {
            'player1': {
                'name': player1.name,
                'team': player1.team.name if player1.team else 'N/A',
                'role': player1.role,
                'stats': {
                    'matches': player1_stats.matches if player1_stats else 0,
                    'runs': player1_stats.runs if player1_stats else 0,
                    'wickets': player1_stats.wickets if player1_stats else 0,
                    'average': player1_stats.average if player1_stats else 0,
                    'strike_rate': player1_stats.strike_rate if player1_stats else 0,
                    'economy': player1_stats.economy if player1_stats else 0
                } if player1_stats else None,
                'tournament_stats': player1_tournament
            },
            'player2': {
                'name': player2.name,
                'team': player2.team.name if player2.team else 'N/A',
                'role': player2.role,
                'stats': {
                    'matches': player2_stats.matches if player2_stats else 0,
                    'runs': player2_stats.runs if player2_stats else 0,
                    'wickets': player2_stats.wickets if player2_stats else 0,
                    'average': player2_stats.average if player2_stats else 0,
                    'strike_rate': player2_stats.strike_rate if player2_stats else 0,
                    'economy': player2_stats.economy if player2_stats else 0
                } if player2_stats else None,
                'tournament_stats': player2_tournament
            }
        }
        
        return JsonResponse(response_data)
        
    except Player.DoesNotExist:
        return JsonResponse({'error': 'One or both players not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_tournament_players(request):
    tournament_id = request.GET.get('tournament', '1')
    player_type = request.GET.get('type', 'batsmen')
    
    try:
        tournament_data = get_tournament_data()
        tournament_info = tournament_data.get(tournament_id, {})
        
        players = tournament_info.get(player_type, [])
        return JsonResponse({'players': players})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 