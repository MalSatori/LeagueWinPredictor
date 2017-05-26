from WinEstimate import RiotAPI
import json
from pprint import pprint
import os
import time


def main():
    api = RiotAPI('key')
    # api = RiotAPI('key')
    get_matches(api)
    get_summonerIDs(api)
    get_matchIDs(api)
    retrieve_matches(api)
    get_stats_from_matches()


def hold():
    while not RiotAPI('key').can_make_request():
        time.sleep(1)

#This pulls the matches from the Riot API.
def get_matches(api):
    with open(os.path.join(os.path.dirname(__file__), 'training_data', 'matchIDs.txt'), 'r+') as file:
        for h in file:
            match = h.rstrip()
            try:
                with open(os.path.join(os.path.dirname(__file__), 'training_data/matches', match + '.txt'), 'x') as file:
                    print('Pulling match #' + match)
                    hold()
                    h = api.get_match_by_id(match)
                    if not h == 0:
                        json.dump(h, file, indent=4)
                        with open(os.path.join(os.path.dirname(__file__), 'training_data/matches_for_training/', match + '.txt.'), 'a+') as f:
                            json.dump(h, f, indent=4)
                        for m in h['participantIdentities']:
                            with open(os.path.join(os.path.dirname(__file__), 'training_data', 'summonerIDs.txt'),
                                      'a+') as file:
                                for line in file:
                                    if str(m['player']['summonerId']) in line:
                                        break
                                else:
                                    file.write(str(m['player']['summonerId']) + '\n')
                    else:
                        file.close()
                        os.remove(os.path.join(os.path.dirname(__file__), 'training_data/matches', match + '.txt'))
            except OSError as e:
                if e.errno != 17:
                    raise
                pass
    get_summonerIDs(api)


#This pulls the match history of a summoner from the Riot API.
def get_matchIDs(api):
    apir = RiotAPI('key', 'na')
    with open(os.path.join(os.path.dirname(__file__), 'training_data', 'summonerIDs.txt'), 'r+') as file:
        for line in file:
            summoner = line.rstrip()
            print('Pulling summoner #' + summoner)
            try:
                with open(os.path.join(os.path.dirname(__file__), 'training_data/summoners/', summoner + '.txt'), 'x') as f:
                    hold()
                    t = apir.get_matches_by_id(summoner)
                    if t != 0:
                        json.dump(t, f, indent=4)
                        for m in t['matches']:
                            if m['queue'] == 'TEAM_BUILDER_RANKED_SOLO' or m['queue'] == 'RANKED_FLEX_SR':
                                with open(os.path.join(os.path.dirname(__file__), 'training_data',
                                                       'matchIDs.txt'), 'a+') as file:
                                    for line in file:
                                        if str(m['matchId']) in line:
                                            break
                                    else:
                                        file.write(str(m['matchId']) + '\n')
                    else:
                        f.close()
                        os.remove(os.path.join(os.path.dirname(__file__), 'training_data/summoners/', summoner + '.txt'))
            except OSError as e:
                if e.errno != 17:
                    raise
                pass
            except KeyError as e:
                if e == 'matches':
                    raise
                pass
    get_matches(api)

if __name__ == "__main__":
    main()