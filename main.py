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
    get_stats_from_matches()
    retrieve_matches()
    get_summonerIDs()


class APIError(Exception):
    """
    Args:
        message (str): the error message
        error_code (int): the HTTP error code that was received
    """
    def __init__(self, message, error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


def get_matches(api):
    with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data', 'matchIDs.txt'), 'r+') as file:
        for h in file:
            match = h.rstrip()
            #print(match)
            try:
                with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/matches', match + '.txt'), 'x') as file:
                    h = api.get_match_by_id(match)
                    if not h == 0:
                        json.dump(h, file, indent=4)
                        with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/matches_for_training/', match + '.txt.'), 'a+') as f:
                            json.dump(h, f, indent=4)
                    else:
                        file.close()
                        os.remove(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/matches', match + '.txt'))
            except OSError as e:
                if e.errno != 17:
                    raise
                pass


def get_summonerIDs():
    for filename in os.listdir('Z:/Homebrew Programs/Python/WinEstimate/training_data/matches/'):
        with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/matches/', filename), 'r') as j:
            i = json.load(j)
            #print(filename)
            for m in i['participantIdentities']:
                with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data', 'summonerIDs.txt'), 'a+') as file:
                    for line in file:
                        if str(m['player']['summonerId']) in line:
                            break
                    else:
                        file.write(str(m['player']['summonerId']) + '\n')


def get_matchIDs(api):
    apir = RiotAPI('RGAPI-dd446914-d130-4817-a1c2-bad4d08ed858', 'na')
    with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data', 'summonerIDs.txt'), 'r+') as file:
        for line in file:
            summoner = line.rstrip()
            try:
                with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/summoners/', summoner + '.txt'), 'x') as f:
                    t = apir.get_matches_by_id(summoner)
                    if t != 0:
                        json.dump(t, f, indent=4)
                        for m in t['matches']:
                            if m['queue'] == 'TEAM_BUILDER_RANKED_SOLO' or m['queue'] == 'RANKED_FLEX_SR':
                                with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data',
                                                       'matchIDs.txt'), 'a+') as file:
                                    for line in file:
                                        if str(m['matchId']) in line:
                                            break
                                    else:
                                        file.write(str(m['matchId']) + '\n')
                    else:
                        f.close()
                        os.remove(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/summoners/', summoner + '.txt'))
            except OSError as e:
                if e.errno != 17:
                    raise
                pass
            except KeyError as e:
                if e == 'matches':
                    raise
                pass


def retrieve_matches():
    for summoner in os.listdir('Z:/Homebrew Programs/Python/WinEstimate/training_data/summoners/'):
        with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/summoners/', summoner), 'r+') as f:
            #print(summoner)
            t = json.load(f)
            for m in t['matches']:
                if m['queue'] == 'TEAM_BUILDER_RANKED_SOLO' or m['queue'] == 'RANKED_FLEX_SR':
                    with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data', 'matchIDs.txt'), 'a+') as file:
                        for line in file:
                            if str(m['matchId']) in line:
                                break
                        else:
                            file.write(str(m['matchId']) + '\n')


def get_stats_from_matches():
    for match in os.listdir('Z:/Homebrew Programs/Python/WinEstimate/training_data/matches_for_training/'):
        with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/matches_for_training/', match), 'r+') as f:
            t = json.load(f)
            for m in t['participants']:
                with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/input_layer', 'input.txt'), 'a+') as file:
                    if m != 10:
                        file.write(str(m['championId']) + ',' + str(m['stats']['kills']) + ',' + str(m['stats']['deaths']) + ',' + str(m['stats']['assists']) + ',')
                    else:
                        file.write(str(m['championId']) + ',' + str(m['stats']['kills']) + ',' + str(m['stats']['deaths']) + ',' + str(m['stats']['assists']))
            with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/input_layer', 'input.txt'), 'a+') as file:
                file.write('\n')
            for m in t['teams']:
                with open(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/input_layer', 'output.txt'), 'a+') as file:
                    if m['win'] == 'Win' and m == 0:
                        file.write('1\n')
                    else:
                        file.write('0\n')
        os.remove(os.path.join('Z:/Homebrew Programs/Python/WinEstimate/training_data/matches_for_training/', match))


if __name__ == "__main__":
    main()