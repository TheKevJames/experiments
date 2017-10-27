#!/usr/bin/env python3
import json

import requests


def as_gold(value):
    value = int(value)

    bronze = value % 100
    silver = (value // 100) % 100
    gold = (value // 100) // 100

    value_string = ''
    if gold:
        value_string += '{}g '.format(gold)
    if silver:
        value_string += '{:02d}s '.format(silver)

    return '{}{:02d}b'.format(value_string, bronze)


LOOKUP_ID = {}
def get_id(name):
    iid = LOOKUP_ID.get(name)
    if iid:
        return iid

    url = 'http://www.gw2spidy.com/api/v0.9/json/item-search/{}/1'.format(name)
    resp = requests.get(url)

    results = resp.json()['results']
    for result in results:
        if result['name'] != name:
            continue

        LOOKUP_ID[name] = result['data_id']
        return result['data_id']

    print(results)
    raise Exception('Could not find ID for item "{}"'.format(name))


# TODO: ensure listings > amount selling
LOOKUP_PRICE = {}
def get_price(iid):
    price = LOOKUP_PRICE.get(iid)
    if price:
        return price

    url = 'https://api.guildwars2.com/v2/commerce/listings/{}'.format(iid)
    resp = requests.get(url).json()

    data = {
        'buy_price': 0,
        'sell_price': float('inf'),
        'sell_profit': 0,
    }

    try:
        for buy in resp['buys']:
            data['buy_price'] = max(data['buy_price'], buy['unit_price'])

        for sell in resp['sells']:
            data['sell_price'] = min(data['sell_price'], sell['unit_price'])

        data['buy_profit'] = round(0.85 * data['buy_price'])
        data['sell_profit'] = round(0.85 * (data['sell_price'] - 1))
    except KeyError:
        # not on TP
        pass

    LOOKUP_PRICE[iid] = data
    return data


def main():
    with open('fractals.json', 'r') as f:
        data = json.load(f)

    lowest = float('inf')
    highest = 0
    average = 0
    for datum in data:
        datum['price'] = 0

        aid = get_id('+1 Agony Infusion')
        datum['price'] += get_price(aid)['sell_profit'] * datum['ar']

        datum['price'] += datum['trash'] * 100

        mat5 = datum.get('5xmat')
        if mat5:
            mid = get_id(mat5)
            datum['price'] += get_price(mid)['sell_profit'] * 5

        mat15 = datum.get('15xmat')
        if mat15:
            mid = get_id(mat15)
            datum['price'] += get_price(mid)['sell_profit'] * 15

        mat50 = datum.get('50xmat')
        if mat50:
            mid = get_id(mat50)
            datum['price'] += get_price(mid)['sell_profit'] * 50

        if datum.get('mew'):
            mid = get_id('Mini Professor Mew')
            datum['price'] += get_price(mid)['sell_profit'] * 50

        recipe = datum.get('recipe')
        if recipe:
            mid = get_id('Recipe: {}'.format(recipe))
            datum['price'] += get_price(mid)['sell_profit']

        # TODO: keys

        lowest = min(lowest, datum['price'])
        highest = max(highest, datum['price'])
        average += datum['price'] / len(data)

    print('Data collected from {} Fractal Encryptions'.format(len(data)))
    print()

    print('Lowest Return: {}'.format(as_gold(lowest)))
    print('Average Return: {}'.format(as_gold(average)))
    print('Highest Return: {}'.format(as_gold(highest)))
    print()

    mid = get_id('Fractal Encryption')
    box_cost = get_price(mid)['buy_price']

    deeply_discounted_key = 2000
    discounted_key = 2540
    key = 3000

    print('Deeply Discounted Key + box: {}'.format(
        as_gold(box_cost + deeply_discounted_key)))
    print('Discounted Key + box: {}'.format(
        as_gold(box_cost + discounted_key)))
    print('Key + box: {}'.format(
        as_gold(box_cost + key)))


if __name__ == '__main__':
    main()
