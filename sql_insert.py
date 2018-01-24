import os
import sqlite3
import json
from datetime import datetime
from pprint import pprint
from WinEstimate import RiotAPI
import time
import pandas as pd

path = 'Z:/Homebrew Programs/Python/leagueSummonerIDs/dbs/'
sql_transaction = []
start_row = 0

connection = sqlite3.connect('{}.db'.format('league'))
connection.isolation_level = None
c = connection.cursor()
row_counter = 0


def create_tables():
    create_match_table()
    create_match_history_table()


def create_match_history_table():
    c.execute("CREATE TABLE IF NOT EXISTS match_player(account_id INT, match_id INT PRIMARY KEY, lane TEXT, champion INT, season INT, queue INT, role TEXT, timestamp INT)")


def create_match_table():
    c.execute("CREATE TABLE IF NOT EXISTS match_info(match_id INT PRIMARY KEY, queue_id INT, season_id INT, p_name_1 TEXT, p_account_id_1 INT, p_summoner_id_1 INT, p_champion_1 INT, \
                p_name_2 TEXT, p_account_id_2 INT, p_summoner_id_2 INT, p_champion_2 INT, p_name_3 TEXT, p_account_id_3 INT, p_summoner_id_3 INT, p_champion_3 INT, \
                p_name_4 TEXT, p_account_id_4 INT, p_summoner_id_4 INT, p_champion_4 INT, p_name_5 TEXT, p_account_id_5 INT, p_summoner_id_5 INT, p_champion_5 INT, \
                p_name_6 TEXT, p_account_id_6 INT, p_summoner_id_6 INT, p_champion_6 INT, p_name_7 TEXT, p_account_id_7 INT, p_summoner_id_7 INT, p_champion_7 INT,\
                p_name_8 TEXT, p_account_id_8 INT, p_summoner_id_8 INT, p_champion_8 INT,p_name_9 TEXT, p_account_id_9 INT, p_summoner_id_9 INT, p_champion_9 INT, \
                p_name_10 TEXT, p_account_id_10 INT, p_summoner_id_10 INT, p_champion_10 INT, game_version TEXT, game_mode TEXT, map_id INT, game_type TEXT, winner TEXT, game_creation INT)")


def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except Exception as e:
                print('Error: ' + e)
                pass
        connection.commit()
        sql_transaction = []


def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id = ?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))


def sql_insert_match_info(match_id, queue_id, season_id, p_name_1, p_account_id_1, p_summoner_id_1, p_champion_1, p_name_2, p_account_id_2, p_summoner_id_2, p_champion_2, \
                p_name_3, p_account_id_3, p_summoner_id_3, p_champion_3, p_name_4, p_account_id_4, p_summoner_id_4, p_champion_4, p_name_5, p_account_id_5, p_summoner_id_5, p_champion_5, \
                p_name_6, p_account_id_6, p_summoner_id_6, p_champion_6, p_name_7, p_account_id_7, p_summoner_id_7, p_champion_7, p_name_8, p_account_id_8, p_summoner_id_8, p_champion_8, \
                p_name_9, p_account_id_9, p_summoner_id_9, p_champion_9, p_name_10, p_account_id_10, p_summoner_id_10, p_champion_10, game_version, game_mode, map_id, game_type, winner, game_creation):
    try:
        sql = """INSERT INTO match_info (match_id, queue_id, season_id, p_name_1, p_account_id_1, p_summoner_id_1, p_champion_1, p_name_2, p_account_id_2, p_summoner_id_2, p_champion_2, \
                p_name_3, p_account_id_3, p_summoner_id_3, p_champion_3, p_name_4, p_account_id_4, p_summoner_id_4, p_champion_4, p_name_5, p_account_id_5, p_summoner_id_5, p_champion_5, \
                p_name_6, p_account_id_6, p_summoner_id_6, p_champion_6, p_name_7, p_account_id_7, p_summoner_id_7, p_champion_7, p_name_8, p_account_id_8, p_summoner_id_8, p_champion_8, \
                p_name_9, p_account_id_9, p_summoner_id_9, p_champion_9, p_name_10, p_account_id_10, p_summoner_id_10, p_champion_10, game_version, game_mode, map_id, game_type, winner, game_creation \
                ) VALUES ({},{},{},"{}",{},{},{},"{}",{},{},{},"{}",{},{},{},"{}",{},{},{},"{}",{},{},{},"{}",{},{},{},"{}",{},{},{},"{}",{},{},{},"{}",{},{},{},"{}",{},{},{},"{}","{}",{},"{}","{}",{} \
                );""".format(match_id, queue_id, season_id, p_name_1, p_account_id_1, p_summoner_id_1, p_champion_1, p_name_2, p_account_id_2, p_summoner_id_2, p_champion_2, \
                p_name_3, p_account_id_3, p_summoner_id_3, p_champion_3, p_name_4, p_account_id_4, p_summoner_id_4, p_champion_4, p_name_5, p_account_id_5, p_summoner_id_5, p_champion_5, \
                p_name_6, p_account_id_6, p_summoner_id_6, p_champion_6, p_name_7, p_account_id_7, p_summoner_id_7, p_champion_7, p_name_8, p_account_id_8, p_summoner_id_8, p_champion_8, \
                p_name_9, p_account_id_9, p_summoner_id_9, p_champion_9, p_name_10, p_account_id_10, p_summoner_id_10, p_champion_10, game_version, game_mode, map_id, game_type, winner, game_creation)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))


def sql_insert_account_info(account_id, match_id, lane, champion, season, queue, role, timestamp):
    try:
        sql = """INSERT INTO match_player (account_id, match_id, lane, champion, season, queue, role, timestamp) \
        VALUES ({},{},"{}",{},{},{},"{}","{}");""".format(account_id, match_id, lane, champion, season, queue, role, timestamp)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))


def hold(key):
    while not RiotAPI(key).can_make_request():
        time.sleep(1)


def main():
    api = RiotAPI()
    create_tables()
    while True:
        get_matchmade_games(api)
        get_summoner_match_history(api)
        #get_summoner_match_history(api)
        #get_matchmade_games(api)
        #pull_account_and_summoner_ids()
        #pull_match_ids()
    # get_summonerIDs(api)
    # retrieve_matches(api)
    # get_stats_from_matches()


def get_matchmade_games(api):
    global row_counter
    limit = 5000
    df = pd.read_sql("SELECT match_id FROM match_player ORDER BY match_id DESC LIMIT {}".format(limit), connection)
    for name, row in df.iterrows():
        matchid = row['match_id']
        while True:
            try:
                hold(api)
                match = api.get_match_by_match_id(matchid)
                if not match == 0:
                    if match['mapId'] == 11:
                        print(match['mapId'])
                        match_id = match['gameId']
                        queue_id = match['queueId']
                        season_id = match['seasonId']
                        p_name_1 = match['participantIdentities'][0]['player']['summonerName']
                        p_account_id_1 = match['participantIdentities'][0]['player']['accountId']
                        p_summoner_id_1 = match['participantIdentities'][0]['player']['summonerId']
                        p_champion_1 = match['participants'][0]['championId']
                        p_name_2 = match['participantIdentities'][1]['player']['summonerName']
                        p_account_id_2 = match['participantIdentities'][1]['player']['accountId']
                        p_summoner_id_2 = match['participantIdentities'][1]['player']['summonerId']
                        p_champion_2 = match['participants'][1]['championId']
                        p_name_3 = match['participantIdentities'][2]['player']['summonerName']
                        p_account_id_3 = match['participantIdentities'][2]['player']['accountId']
                        p_summoner_id_3 = match['participantIdentities'][2]['player']['summonerId']
                        p_champion_3 = match['participants'][2]['championId']
                        p_name_4 = match['participantIdentities'][3]['player']['summonerName']
                        p_account_id_4 = match['participantIdentities'][3]['player']['accountId']
                        p_summoner_id_4 = match['participantIdentities'][3]['player']['summonerId']
                        p_champion_4 = match['participants'][3]['championId']
                        p_name_5 = match['participantIdentities'][4]['player']['summonerName']
                        p_account_id_5 = match['participantIdentities'][4]['player']['accountId']
                        p_summoner_id_5 = match['participantIdentities'][4]['player']['summonerId']
                        p_champion_5 = match['participants'][4]['championId']
                        p_name_6 = match['participantIdentities'][5]['player']['summonerName']
                        p_account_id_6 = match['participantIdentities'][5]['player']['accountId']
                        p_summoner_id_6 = match['participantIdentities'][5]['player']['summonerId']
                        p_champion_6 = match['participants'][5]['championId']
                        p_name_7 = match['participantIdentities'][6]['player']['summonerName']
                        p_account_id_7 = match['participantIdentities'][6]['player']['accountId']
                        p_summoner_id_7 = match['participantIdentities'][6]['player']['summonerId']
                        p_champion_7 = match['participants'][6]['championId']
                        p_name_8 = match['participantIdentities'][7]['player']['summonerName']
                        p_account_id_8 = match['participantIdentities'][7]['player']['accountId']
                        p_summoner_id_8 = match['participantIdentities'][7]['player']['summonerId']
                        p_champion_8 = match['participants'][7]['championId']
                        p_name_9 = match['participantIdentities'][8]['player']['summonerName']
                        p_account_id_9 = match['participantIdentities'][8]['player']['accountId']
                        p_summoner_id_9 = match['participantIdentities'][8]['player']['summonerId']
                        p_champion_9 = match['participants'][8]['championId']
                        p_name_10 = match['participantIdentities'][9]['player']['summonerName']
                        p_account_id_10 = match['participantIdentities'][9]['player']['accountId']
                        p_summoner_id_10 = match['participantIdentities'][9]['player']['summonerId']
                        p_champion_10 = match['participants'][9]['championId']
                        game_version = match['gameVersion']
                        game_mode = match['gameMode']
                        map_id = match['mapId']
                        game_type = match['gameType']
                        if match['teams'][0]['win'] == 'Win':
                            winner = 'Blue'
                        else:
                            winner = 'Red'
                        game_creation = match['gameCreation']

                        sql_insert_match_info(match_id, queue_id, season_id, p_name_1, p_account_id_1, p_summoner_id_1, p_champion_1, p_name_2, p_account_id_2, p_summoner_id_2, p_champion_2, \
                        p_name_3, p_account_id_3, p_summoner_id_3, p_champion_3, p_name_4, p_account_id_4, p_summoner_id_4, p_champion_4, p_name_5, p_account_id_5, p_summoner_id_5, p_champion_5, \
                        p_name_6, p_account_id_6, p_summoner_id_6, p_champion_6, p_name_7, p_account_id_7, p_summoner_id_7, p_champion_7, p_name_8, p_account_id_8, p_summoner_id_8, p_champion_8, \
                        p_name_9, p_account_id_9, p_summoner_id_9, p_champion_9, p_name_10, p_account_id_10, p_summoner_id_10, p_champion_10, game_version, game_mode, map_id, game_type, winner, game_creation)

                        row_counter += 1
                        if row_counter % 10000 == 0:
                                    print('Total rows: {}'.format(row_counter))

            except ConnectionError as e:
                time.sleep(1)
                continue
            break


def get_summoner_match_history(api):
    global row_counter
    limit = 5000
    accounts = []
    df = pd.read_sql("SELECT * FROM match_info ORDER BY match_id DESC LIMIT {}".format(limit), connection)
    for name, row in df.iterrows():
        accounts.append(row['p_account_id_1'])
        accounts.append(row['p_account_id_2'])
        accounts.append(row['p_account_id_3'])
        accounts.append(row['p_account_id_4'])
        accounts.append(row['p_account_id_5'])
        accounts.append(row['p_account_id_6'])
        accounts.append(row['p_account_id_7'])
        accounts.append(row['p_account_id_8'])
        accounts.append(row['p_account_id_9'])
        accounts.append(row['p_account_id_10'])

        for account in accounts:
            while True:
                try:
                    hold(api)
                    match_history = api.get_summoner_match_history(account)
                    if not match_history == 0:
                        for x in match_history['matches']:
                            account_id = account
                            match_id = x['gameId']
                            lane = x['lane']
                            champion = x['champion']
                            season = x['season']
                            queue = x['queue']
                            role = x['role']
                            timestamp = x['timestamp']

                            sql_insert_account_info(account_id, match_id, lane, champion, season, queue, role, timestamp)
                            row_counter += 1
                            if row_counter % 10000 == 0:
                                print('Total rows: {}'.format(row_counter))

                except ConnectionError as e:
                    time.sleep(1)
                    continue
                except KeyError as e:
                    pass
                break


def get_champ_mastery_details(api):
    for summoner in summoner_id.find({}, {'summoner_id': 1, '_id': 0}, no_cursor_timeout=True):
        try:
            summoner = summoner['summoner_id']
            print('Pulling summoner #' + str(summoner) + '.')
            hold(api) # Rate limiting.
            champion_mastery = api.get_mastery_by_summoner_id(summoner) # API Call.
            if not champion_mastery == 0: # Make sure something was returned.
                print('Summoner #' + str(summoner))
                champion_mastery.update({'summoner_id': summoner}) # Add summoner ID to the mastery JSON.
                mastery.update({'summoner_id': summoner}, champion_mastery, upsert=True) # Inserts account mastery in DB
                account_id.delete_many({'summoner_id': summoner}) # Deletes the account ID from the list of account IDs
        except KeyError as e:
            print(e)
            pass
        except pymongo.errors.DuplicateKeyError as e:
            # print(e)
            pass


main()
