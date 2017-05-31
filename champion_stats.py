import csv
import os
import json


champs = []


def get_champs():
    # for match in os.listdir(os.path.dirname(__file__) + '/training_data/matches/'):
    #     with open(os.path.join(os.path.dirname(__file__), 'training_data/matches/', match), 'r+') as f:
    #         try:
    #             k = json.load(f)
    #         except json.decoder.JSONDecodeError as e:
    #             print(e)
    #             f.close()
    #             os.remove(os.path.join(os.path.dirname(__file__), 'training_data/matches/', match))
    #         print(match)
    #         if k['mapId'] == 10:
    #             f.close()
    #             os.remove(os.path.join(os.path.dirname(__file__), 'training_data/matches/', match))

    for matchID in os.listdir('training_data/matches/'):
        with open(os.path.join(os.path.dirname(__file__), 'training_data/matchIDs.txt'), 'a+') as j:
            matchID = matchID[:-4]
            j.write(matchID + '\n')


    # with open(os.path.join(os.path.dirname(__file__), 'training_data', 'champ_nums.txt'), 'r+') as file:
    #     for l in file.read().strip().split(','):
    #         champs.append(l)
    #
    # with open(os.path.join(os.path.dirname(__file__), 'training_data', 'summonerIDs.txt'), 'r+') as file:
    #     for line in file:
    #         summoner = line.rstrip()
    #         with open(os.path.join(os.path.dirname(__file__), 'training_data/summoners/', summoner + '.txt'), 'r+') as f:
    #             k = json.load(f)
    #             matches = []
    #             champ_games_played = []
    #             wins = []
    #             losses = []
    #             total_games = 0
    #             print(summoner)
    #             try:
    #                 for m in k['matches']:
    #                     matches.append(m['matchId'])
    #                 for x in matches:
    #                     with open(os.path.join(os.path.dirname(__file__), 'training_data/matches/', str(x) + '.txt'), 'r+') as g:
    #                         l = json.load(g)
    #
    #
    #             except KeyError:
    #                 pass


get_champs()