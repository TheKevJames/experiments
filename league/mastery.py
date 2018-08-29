#!/usr/bin/env python3
import collections
import os
import pprint
import time

import requests


API_BASE_URL = 'https://na1.api.riotgames.com'
DD_BASE_URL = 'https://ddragon.leagueoflegends.com/cdn/8.14.1'

LEAGUE_TOKEN = os.environ['LEAGUE_TOKEN']
ACCOUNT_ID = '36860315'   # Kevin
ACCOUNT_ID = '231362490'  # Lara
ACCOUNT_ID = '32797805'   # OT
ACCOUNT_ID = '32971449'   # doublelift
ACCOUNT_ID = '29512'      # pobelter
ACCOUNT_ID = '469064'     # aphromoo
ACCOUNT_ID = '223306587'  # huhi


def get_champs():
    url = f'{DD_BASE_URL}/data/en_US/champion.json'

    resp = requests.get(url)
    resp.raise_for_status()
    lookup = {int(c['key']): c['name'] for c in resp.json()['data'].values()}
    return lookup


def get_matches(seasons=None):
    url = f'{API_BASE_URL}/lol/match/v3/matchlists/by-account/{ACCOUNT_ID}'
    headers = {'X-Riot-Token': LEAGUE_TOKEN}
    params = {
        'beginIndex': 0,
        'queue': {420, 440},
        'season': seasons or {10, 11},
    }

    while True:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        if data['endIndex'] == data['startIndex']:
            break

        params['beginIndex'] += 100
        yield from data['matches']


def main():
    champs = get_champs()
    pool = set()

    playrates = collections.Counter(champs[x['champion']]
                                    for x in get_matches(seasons={10, 11}))
    # lara
    # playrates = collections.Counter({'Morgana': 275, 'Leona': 32, 'Lulu': 31, 'Soraka': 28, 'Rakan': 17, 'Nami': 13, 'Bard': 10, 'Tahm Kench': 8, 'Brand': 5, 'Karma': 4, 'Tristana': 3, 'Sona': 3, 'Thresh': 2, 'Taric': 2, 'Alistar': 2, 'Lux': 1, 'Braum': 1, 'Janna': 1, 'Zilean': 1})
    # kevin
    # playrates = collections.Counter({'Caitlyn': 65, 'Morgana': 49, 'Tristana': 38, "Kha'Zix": 32, 'Singed': 29, 'Kindred': 26, 'Swain': 25, 'Viktor': 23, 'Rammus': 16, 'Olaf': 15, 'Vayne': 15, 'Brand': 14, 'Illaoi': 13, 'Blitzcrank': 13, 'Kalista': 12, 'Xerath': 11, 'Fiddlesticks': 11, 'Dr. Mundo': 10, "Kai'Sa": 9, 'Ryze': 9, 'Veigar': 9, 'Draven': 7, "Vel'Koz": 6, 'Nocturne': 5, 'Taliyah': 5, 'Thresh': 5, 'Malzahar': 4, 'Warwick': 4, 'Sion': 4, 'Alistar': 4, 'Gragas': 4, 'Miss Fortune': 4, 'Soraka': 4, 'Teemo': 4, "Cho'Gath": 3, 'Rengar': 3, 'Ashe': 3, 'Jhin': 3, 'Sivir': 3, 'Twitch': 3, 'Karthus': 2, 'Nidalee': 2, 'Twisted Fate': 2, 'Nami': 2, 'Amumu': 2, 'Bard': 2, 'Rakan': 2, 'Rumble': 2, 'Maokai': 2, 'Aatrox': 1, 'Jinx': 1, 'Kled': 1, 'Lee Sin': 1, 'Jayce': 1, 'Irelia': 1, 'Volibear': 1, 'Zyra': 1, 'Kayle': 1, 'Heimerdinger': 1, 'Cassiopeia': 1, 'Gnar': 1, 'Nasus': 1, 'Galio': 1})
    pool.update({k for k, v in playrates.items() if v >= 5})
    # TODO: filter by winrate >= 45%

    time.sleep(3)

    # playrates = collections.Counter(champs[x['champion']]
    #                                 for x in get_matches(seasons={8, 9}))
    # lara
    # playrates = collections.Counter({'Morgana': 36, 'Soraka': 17, 'Lulu': 14, 'Karma': 7, 'Sona': 6, 'Bard': 4, 'Miss Fortune': 3, 'Zilean': 2, 'Leona': 2, 'Tahm Kench': 1, 'Taric': 1})
    # kevin
    # playrates = collections.Counter({'Morgana': 193, 'Caitlyn': 73, 'Tristana': 72, 'Singed': 63, "Kha'Zix": 45, 'Sion': 45, 'Brand': 33, 'Veigar': 32, 'Zyra': 28, 'Kindred': 27, 'Swain': 25, 'Alistar': 25, 'Viktor': 23, 'Blitzcrank': 21, "Cho'Gath": 19, 'Rammus': 19, 'Amumu': 19, 'Thresh': 17, 'Dr. Mundo': 16, 'Olaf': 15, 'Vayne': 15, 'Ashe': 15, 'Bard': 15, 'Illaoi': 14, 'Fiddlesticks': 14, 'Gragas': 13, 'Kalista': 12, 'Xerath': 11, 'Jinx': 11, 'Soraka': 10, 'Karma': 10, "Kai'Sa": 9, 'Ryze': 9, 'Warwick': 8, 'Rumble': 8, 'Taliyah': 7, 'Draven': 7, "Vel'Koz": 6, 'Nami': 6, 'Teemo': 6, 'Zilean': 6, 'Nocturne': 5, 'Miss Fortune': 5, 'Malzahar': 4, 'Sivir': 4, 'Heimerdinger': 4, 'Nasus': 4, 'Karthus': 3, 'Rengar': 3, 'Nidalee': 3, 'Jhin': 3, 'Twitch': 3, 'Twisted Fate': 2, 'Rakan': 2, 'Maokai': 2, 'Cassiopeia': 2, 'Vladimir': 2, 'Sona': 2, 'Aatrox': 1, 'Kled': 1, 'Lee Sin': 1, 'Jayce': 1, 'Irelia': 1, 'Volibear': 1, 'Kayle': 1, 'Gnar': 1, 'Galio': 1, 'Master Yi': 1, 'Anivia': 1, 'Lux': 1}) - collections.Counter({'Caitlyn': 65, 'Morgana': 49, 'Tristana': 38, "Kha'Zix": 32, 'Singed': 29, 'Kindred': 26, 'Swain': 25, 'Viktor': 23, 'Rammus': 16, 'Olaf': 15, 'Vayne': 15, 'Brand': 14, 'Illaoi': 13, 'Blitzcrank': 13, 'Kalista': 12, 'Xerath': 11, 'Fiddlesticks': 11, 'Dr. Mundo': 10, "Kai'Sa": 9, 'Ryze': 9, 'Veigar': 9, 'Draven': 7, "Vel'Koz": 6, 'Nocturne': 5, 'Taliyah': 5, 'Thresh': 5, 'Malzahar': 4, 'Warwick': 4, 'Sion': 4, 'Alistar': 4, 'Gragas': 4, 'Miss Fortune': 4, 'Soraka': 4, 'Teemo': 4, "Cho'Gath": 3, 'Rengar': 3, 'Ashe': 3, 'Jhin': 3, 'Sivir': 3, 'Twitch': 3, 'Karthus': 2, 'Nidalee': 2, 'Twisted Fate': 2, 'Nami': 2, 'Amumu': 2, 'Bard': 2, 'Rakan': 2, 'Rumble': 2, 'Maokai': 2, 'Aatrox': 1, 'Jinx': 1, 'Kled': 1, 'Lee Sin': 1, 'Jayce': 1, 'Irelia': 1, 'Volibear': 1, 'Zyra': 1, 'Kayle': 1, 'Heimerdinger': 1, 'Cassiopeia': 1, 'Gnar': 1, 'Nasus': 1, 'Galio': 1})
    pool.update({k for k, v in playrates.items() if v >= 20})

    pprint.pprint(sorted(pool))
    print(len(pool))


if __name__ == '__main__':
    main()
