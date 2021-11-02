# ~/Library/Logs/Wizards\ Of\ The\ Coast/MTGA/Player.log

# Exporting deck data to clipboard:

# file to find decks in the mtga logs then upload them to my site.
# bassed off of dirwatcher with an automatic push feature.

import os
import re
import datetime
from badhistoricdecks.models import Deck
import json
os.chdir("../../../Library/Logs/Wizards Of The Coast/MTGA")
# print(os.listdir())
with open("""Player.log""", 'r') as f:
    text = f.read()
    decks = []
    match = re.finditer(r'(Exporting deck)[^[{]+', text)
    os.chdir("/Users/marcuschirirboga/coding/q4/magicsite")
    i = 0
    for item in match:
        i += 1
        # print(item)
        with open(f"localdecks/decktest{i}.dec", 'w+') as f:
            deck = item.group(0).strip().split('\n')
            deck.pop(0)
            sideboard_index = deck.index("Sideboard")
            sideboard = deck[sideboard_index:]
            deck = deck[:sideboard_index]
            deck_dict = dict()
            sb_dict = {}
            for card in deck:
                if not card:
                    continue
                quantity = card[0]
                if quantity.isalpha():
                    continue
                while not card[0].isalpha():
                    card = card[1:]
                while card.find('(') != -1:
                    card = card[:-1]
                deck_dict.update({card: int(quantity)})
            for card in sideboard:
                if not card:
                    continue
                quantity = card[0]
                if quantity.isalpha():
                    continue
                while not card[0].isalpha():
                    card = card[1:]
                while card.find('(') != -1:
                    card = card[:-1]
                sb_dict.update({card: int(quantity)})
            print(deck_dict)
            # f.write(",".join(deck))
            deck_to_save = {"deck": deck_dict, "sideboard": sb_dict}
            print(deck_to_save)
            Deck.objects.create(
                title=f'deck{i}',
                decklist='hold',
                description=str(deck),
                actual_decklist=json(deck_to_save),
            )
            f.write(str(deck_to_save))
