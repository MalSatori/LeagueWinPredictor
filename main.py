from WinEstimate import RiotAPI
import json
from pprint import pprint
import os
import time


def main():
    api = RiotAPI('RGAPI-dd446914-d130-4817-a1c2-bad4d08ed858')
    # api = RiotAPI('RGAPI-826d5283-e20d-4ceb-b890-dc2ce5e91fb9')
    get_matches(api)
    get_matchIDs(api)
    retrieve_matches(api)
    get_summonerIDs(api)
    get_stats_from_matches()


def hold():
    while not RiotAPI('RGAPI-dd446914-d130-4817-a1c2-bad4d08ed858').can_make_request():
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
                    else:
                        file.close()
                        os.remove(os.path.join(os.path.dirname(__file__), 'training_data/matches', match + '.txt'))
            except OSError as e:
                if e.errno != 17:
                    raise
                pass
    get_summonerIDs(api)


#This pulls the summoners from our matches and writes them to a file.
def get_summonerIDs(api):
    for filename in os.listdir(os.path.dirname(__file__), 'training_data/matches/'):
        with open(os.path.join(os.path.dirname(__file__), 'training_data/matches/', filename), 'r') as j:
            i = json.load(j)
            print('Pulling summoners from match: ' + filename)
            for m in i['participantIdentities']:
                with open(os.path.join(os.path.dirname(__file__), 'training_data', 'summonerIDs.txt'), 'a+') as file:
                    for line in file:
                        if str(m['player']['summonerId']) in line:
                            break
                    else:
                        file.write(str(m['player']['summonerId']) + '\n')
    get_matchIDs(api)


#This pulls the match history of a summoner from the Riot API.
def get_matchIDs(api):
    apir = RiotAPI('RGAPI-dd446914-d130-4817-a1c2-bad4d08ed858', 'na')
    with open(os.path.join(os.path.dirname(__file__), 'training_data', 'summonerIDs.txt'), 'r+') as file:
        for line in file:
            summoner = line.rstrip()
            print('Pulling summoner #' + match)
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

#This pulls the ranked matches from a summoner IDs match history and writes them to a file..
def retrieve_matches(api):
    for summoner in os.listdir(os.path.dirname(__file__), 'training_data/summoners/'):
        with open(os.path.join(os.path.dirname(__file__), 'training_data/summoners/', summoner), 'r+') as f:
            print('Pulling matches from summoner #' + summoner)
            t = json.load(f)
            for m in t['matches']:
                if m['queue'] == 'TEAM_BUILDER_RANKED_SOLO' or m['queue'] == 'RANKED_FLEX_SR':
                    with open(os.path.join(os.path.dirname(__file__), 'training_data', 'matchIDs.txt'), 'a+') as file:
                        for line in file:
                            if str(m['matchId']) in line:
                                break
                        else:
                            file.write(str(m['matchId']) + '\n')



#This takes the copy of the matches and puts them in a CSV file that I was planning on running through a neural net.
def get_stats_from_matches():
    for match in os.listdir(os.path.dirname(__file__), 'training_data/matches_for_training/'):
        with open(os.path.join(os.path.dirname(__file__), 'training_data/matches_for_training/', match), 'r+') as f:
            t = json.load(f)
            for m in t['participants']:
                with open(os.path.join(os.path.dirname(__file__), 'training_data/input_layer', 'input.txt'), 'a+') as file:
                    if m != 10:
                        file.write(str(m['championId']) + ',' + str(m['stats']['kills']) + ',' + str(m['stats']['deaths']) + ',' + str(m['stats']['assists']) + ',')
                    else:
                        file.write(str(m['championId']) + ',' + str(m['stats']['kills']) + ',' + str(m['stats']['deaths']) + ',' + str(m['stats']['assists']))
            with open(os.path.join(os.path.dirname(__file__), 'training_data/input_layer', 'input.txt'), 'a+') as file:
                file.write('\n')
            for m in t['teams']:
                with open(os.path.join(os.path.dirname(__file__), 'training_data/input_layer', 'output.txt'), 'a+') as file:
                    if m['win'] == 'Win' and m == 0:
                        file.write('1\n')
                    else:
                        file.write('0\n')
        os.remove(os.path.join(os.path.dirname(__file__), 'training_data/matches_for_training/', match))


if __name__ == "__main__":
    main()