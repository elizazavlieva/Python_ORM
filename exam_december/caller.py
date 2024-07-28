import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import TennisPlayer, Match, Tournament
from django.db.models import Q, Count

def get_tennis_players(search_name=None, search_country=None):

    if search_name is  None and search_country is None:
        return ''

    elif search_name is None:
        query = Q(country__icontains=search_country)

    elif search_country is None:
        query = Q(full_name__icontains=search_name)

    else:
        query = Q(full_name__icontains=search_name) & Q(country__icontains=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    return '\n'.join([f"Tennis Player: {t.full_name}, country: {t.country}, ranking: {t.ranking}"
                      for t in players]) if players else ''


def get_top_tennis_player():
    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    return f"Top Tennis Player: {player.full_name} with {player.win_count} wins." if player else ''


def get_tennis_player_by_matches_count():
    player = TennisPlayer.objects.annotate(matches_count=Count('players')).order_by('-matches_count', 'ranking').first()
    return f"Tennis Player: {player.full_name} with {player.matches_count} matches played." \
        if player and player.matches_count else ''


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ''

    matches = Tournament.objects.prefetch_related('tournaments').annotate(matches_count=Count('tournaments')
                                     ).filter(surface_type__icontains=surface
                                              ).order_by('-start_date')

    return '\n'.join([f"Tournament: {m.name}, start date: "
                      f"{m.start_date}, matches: {m.matches_count}" for m in matches]) if matches else ''


def get_latest_match_info():
    latest_match = Match.objects.prefetch_related('tournament').order_by('-date_played', '-id').first()

    if not latest_match:
        return ''

    winner = latest_match.winner.full_name if latest_match.winner else 'TBA'
    players = f"{latest_match.players.first()} vs {latest_match.players.last()}"

    return (f"Latest match played on: {latest_match.date_played}, "
            f"tournament: {latest_match.tournament.name}, score: {latest_match.score}, "
            f"players: {players}, winner: {winner}, summary: {latest_match.summary}")

print(get_latest_match_info())

def get_matches_by_tournament(tournament_name=None):

    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.select_related('tournament', 'winner').filter(tournament__name__exact=tournament_name
                                                                          ).order_by('-date_played')

    if not matches:
        return "No matches found."

    return '\n'.join([f"Match played on: {m.date_played}, score: {m.score}, "
                      f"winner: {m.winner.full_name if m.winner else 'TBA'}"
                      for m in matches])


