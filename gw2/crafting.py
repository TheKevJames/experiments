#!/usr/bin/env python3
import os

import requests


# TODO: merge with fractals.py
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


# TODO: merge with fractals.py
LOOKUP_PRICE = {}
def get_price(iid):
    price = LOOKUP_PRICE.get(iid)
    if price:
        return price

    url = 'https://api.guildwars2.com/v2/commerce/listings/{}'.format(iid)
    resp = requests.get(url).json()

    data = {
        'buy_price': 0,
        'buy_profit': 0,
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
        # url = 'https://api.guildwars2.com/v2/items/{}'.format(iid)
        # item = requests.get(url).json()
        # print('Error: no data for {}'.format(item['name']))
        return

    LOOKUP_PRICE[iid] = data
    return data


def get_recipes():
    url = 'https://api.guildwars2.com/v2/account/recipes'
    headers = {
        'Authorization': 'Bearer {}'.format(os.environ['GW2_ACCESS_TOKEN']),
    }

    resp = requests.get(url, headers=headers)
    return resp.json()


def main():
    recipes = get_recipes()

    for rid in recipes:
        url = 'https://api.guildwars2.com/v2/recipes/{}'.format(rid)
        recipe = requests.get(url).json()

        try:
            ingred_cost = 0
            for ingredient in recipe['ingredients']:
                # TODO: buy_price for buy offer, sell price for immediate
                buy_cost = get_price(ingredient['item_id'])['sell_price']
                ingred_cost += buy_cost * ingredient['count']

            # TODO: buy_profit for immediate, sell_profit for lowest - 1
            sell_profit = get_price(recipe['output_item_id'])['buy_profit']
            sell_profit *= recipe['output_item_count']
        except TypeError:
            # error fetching ingredient
            continue

        url = 'https://api.guildwars2.com/v2/items/{}'.format(
            recipe['output_item_id'])
        item = requests.get(url).json()

        if sell_profit > ingred_cost:
            print('{} (cost: {}, profit: {})'.format(item['name'],
                                                     as_gold(ingred_cost),
                                                     as_gold(sell_profit)))


if __name__ == '__main__':
    main()
