from typing import Dict, List, Iterable
import sys
import json
from pprint import pprint
from termcolor import colored

import requests

# API docs: https://scryfall.com/docs/api
SCRYFALL_URL = "https://api.scryfall.com"

def format_mana_cost(s: str) -> str:
    """
    >>> assert format_mana_cost("{3}{W}") == "3W"
    """
    return (s
        .replace("{1}", "1")
        .replace("{2}", "2")
        .replace("{3}", "3")
        .replace("{4}", "4")
        .replace("{5}", "5")
        .replace("{6}", "6")
        .replace("{7}", "7")
        .replace("{8}", "8")
        .replace("{8}", "9")
        
        .replace("{W}", "W")
        .replace("{U}", "U")
        .replace("{R}", "R")
        .replace("{B}", "B")
        .replace("{G}", "G")
        
        .replace("W", colored("W", "white"))
        .replace("U", colored("U", "blue"))
        .replace("R", colored("R", "red"))
        .replace("B", colored("B", "cyan"))
        .replace("G", colored("G", "green"))
    )

def format_card_dict(card_dict) -> str:
    """Possible card_dict keys:
    'object', 'id', 'oracle_id', 'multiverse_ids', 'mtgo_id', 'mtgo_foil_id',
    'name', 'lang', 'released_at', 'uri', 'scryfall_uri', 'layout',
    'highres_image', 'image_uris', 'mana_cost', 'cmc', 'type_line',
    'oracle_text', 'colors', 'color_identity', 'legalities', 'games',
    'reserved', 'foil', 'nonfoil', 'oversized', 'promo', 'reprint',
    'variation', 'set', 'set_name', 'set_type', 'set_uri', 'set_search_uri',
    'scryfall_set_uri', 'rulings_uri', 'prints_search_uri', 'collector_number',
    'digital', 'rarity', 'flavor_text', 'illustration_id', 'card_back_id',
    'artist', 'border_color', 'frame', 'full_art', 'textless', 'booster',
    'story_spotlight', 'edhrec_rank', 'prices', 'related_uris', 'purchase_uris'
    """
    raw_mana_cost_string = card_dict.get("mana_cost", "((Unknown mana cost))")
    mana_cost_string = format_mana_cost(raw_mana_cost_string)
    
    return f"""
    {card_dict["name"]} - {mana_cost_string}
    {card_dict.get("oracle_text", "((Unknown oracle text))")}
    """.strip()
    

def call(url_fragment, params=None):
    return requests.get(SCRYFALL_URL + url_fragment,
                        params=params if params else {}).json()
    
def get_search_term() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        return "shock"
    
    
def print_card_info_divider() -> None:
    print("---")
    
def get_cards_info(search_term) -> Iterable[Dict]:
    assert search_term, "search_term must not be empty"
    assert search_term != '""', "search_term must not be empty"
    card_search_dict = call("/cards/search", {"q": search_term})
    
    if card_search_dict.get("code") == "not_found":
        card_dicts: List[Dict] = []
    else:
        if "data" not in card_search_dict:
            raise Exception(
                f"Failed getting card info, response: {card_search_dict}")
        card_dicts: List[Dict] = card_search_dict["data"]
        
    yield from card_dicts
            
def quoted(s: str) -> str:
    return f'"{s}"'

def main():
    while True:
        try:
            card_search_term = input()
        except EOFError:
            return
        
        for card in get_cards_info(search_term=quoted(card_search_term)):
            print(format_card_dict(card))
            print_card_info_divider()

if __name__ == "__main__":
    main()
