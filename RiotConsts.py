import requests as r


URL = {
    'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
    'base1': 'https://{proxy}.api.riotgames.com/lol/{url}',
    'summoner_by_name': 'summoner/v{version}/summoners/by-name/{names}',
    'matches_by_summonerID': 'v{version}/matchlist/by-summoner/{summonerId}',
    'match_stats_from_matchID': 'match/v{version}/matches/{matchId}'
}

API_VERSIONS = {
    'summoner': '3',
    'matches': '2.2',
    'match': '3'
}

REGIONS = {
    'europe_nordic_and_east': 'eune',
    'europe_west': 'euw',
    'north_murica': 'na',
    'north_america': 'na1'
}

SERVER = {
    'riot': 'riotgames',
    'pvp': 'pvp'
}

SERVERTYPE = {
    'riot': 'com',
    'pvp': 'net'
}

summoner_id = 21792220

api_key = 'RGAPI-9a575e99-756f-4899-a124-1ea2dd3bbebb'

