import requests as r
import RiotConsts as riot
import time
from collections import deque


def opt_out(response):
    if response.status_code in [400, 404, 500, 502, 503]:
        print('Got error ' + str(response.status_code) + '. Moving on.')
        return False
    if response.status_code in [403,429]:
        print('Got a ' + str(response.status_code) + '. Pausing for ' + response.headers['Retry-After'] + 'seconds.')
        time.sleep(int(response.headers['Retry-After']))
        return False
    return True



class RateLimit:
    def __init__(self, allowed_requests, seconds):
        self.allowed_requests = allowed_requests
        self.seconds = seconds
        self.made_requests = deque()

    def __reload(self):
        t = time.time()
        while len(self.made_requests) > 0 and self.made_requests[0] < t:
            self.made_requests.popleft()

    def add_request(self):
        self.made_requests.append(time.time() + self.seconds)

    def request_available(self):
        self.__reload()
        return len(self.made_requests) < self.allowed_requests


class RiotAPI(object):
    def __init__(self, api_key, region=riot.REGIONS['north_america'], limits=(RateLimit(5, 6), RateLimit(500, 600), )):
        self.api_key = api_key
        self.region = region
        self.limits = limits

    def can_make_request(self):
        for lim in self.limits:
            if not lim.request_available():
                return False
            return True

    def _requests(self, api_url, base, params={}, static=False):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = r.get(
            riot.URL[base].format(
                proxy=self.region,
                region=self.region,
                url=api_url
            ),
            params=args
        )

        if not static:
            for lim in self.limits:
                lim.add_request()
        if opt_out(response) == False:
            return 0
        else:
            return response.json()

    def get_summoner_by_name(self, name):
        api_url = riot.URL['summoner_by_name'].format(
            version=riot.API_VERSIONS['summoner'],
            names=name
        )
        return self._requests(api_url, 'base1')

    def get_matches_by_id(self, id):
        api_url = riot.URL['matches_by_summonerID'].format(
            version=riot.API_VERSIONS['matches'],
            summonerId=id
        )
        return self._requests(api_url, 'base')

    def get_match_by_id(self, id):
        api_url = riot.URL['match_stats_from_matchID'].format(
            version=riot.API_VERSIONS['match'],
            matchId=id
        )
        return self._requests(api_url, 'base1')