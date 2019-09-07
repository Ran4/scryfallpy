from typing import Dict, List, Iterable, Callable
import sys
import json
from pprint import pprint
from termcolor import colored
import urllib
    

import argumentparsing

import requests

# API docs: https://scryfall.com/docs/api
SCRYFALL_URL = "https://api.scryfall.com"

def format_mana_cost(s: str, colored_func: Callable) -> str:
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
        
        .replace("W", colored_func("W", "white"))
        .replace("U", colored_func("U", "blue"))
        .replace("R", colored_func("R", "red"))
        .replace("B", colored_func("B", "cyan"))
        .replace("G", colored_func("G", "green"))
    )

def format_card_dict(card_dict, args) -> str:
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
    colored_func: Callable = (lambda s, *_args: s) if args.no_color else colored
    mana_cost_string = format_mana_cost(raw_mana_cost_string, colored_func)
    
    if "toughness" in card_dict and "power" in card_dict:
        power: str = card_dict["power"]
        toughness: str = card_dict["toughness"]
        creature_stats = f'\n{power}/{toughness}'
    else:
        creature_stats = ""
    
    return f"""
    {card_dict["name"]} - {mana_cost_string}
    {card_dict.get("oracle_text", "((Unknown oracle text))")}{creature_stats}
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
    card_search_dict = call("/cards/search", {"q": search_term + " f:standard"})
    
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


def print_cards_from_stdin(args):
    while True:
        try:
            card_search_term = input()
        except EOFError:
            return
        
        for card in get_cards_info(search_term=quoted(card_search_term)):
            print(format_card_dict(card, args))
            print_card_info_divider()
            
def get_search_term_from_stdin() -> List[str]:
    card_search_terms = []
    while True:
        try:
            card_search_term = input().strip()
        except EOFError:
            break
        card_search_terms.append(card_search_term)
    return card_search_terms
            
def print_url_from_stdin():
    search_terms: List[str] = get_search_term_from_stdin()
    EXACT_NAME_MATCH_PREFIX = "!"
    
    
    #~ ns = []
    #~ for search_term in search_terms:
    #~     if search_term:
    #~         ns.append(EXACT_NAME_MATCH_PREFIX + quoted(search_term.strip()))
    #~         print(ns[-1])
    #~ stripped_and_quoted_search_terms = ns

    
    stripped_and_quoted_search_terms: List[str] = \
        [EXACT_NAME_MATCH_PREFIX + quoted(search_term.strip())
         for search_term in search_terms
         if search_term.strip()]
    #~ for x in stripped_and_quoted_search_terms:
    #~     print(x)
    #~ exit()
    search_term_string: str = " OR ".join(stripped_and_quoted_search_terms)
    url_encoded_search_term_string: str = urllib.parse.quote(search_term_string)
    url = f"https://scryfall.com/search?q=" + url_encoded_search_term_string
    print(url)

def main():
    args = argumentparsing.get_args()
    
    if args.print_url:
        print_url_from_stdin()
    else:
        print_cards_from_stdin(args)

if __name__ == "__main__":
    main()
