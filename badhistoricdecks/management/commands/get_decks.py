import datetime
import re
import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import query
from django.db.models.query_utils import Q
from badhistoricdecks.models import Deck, User
from cardhandler.models import Card
import json


class Command(BaseCommand):
    help = 'bootstrap to populate dropdown'

    def handle(self, *args, **options):
        # deleteables = Deck.objects.all()
        # deleteables.delete()

        # ~/Library/Logs/Wizards\ Of\ The\ Coast/MTGA/Player.log

        # "Exporting deck data to clipboard:""

        # file to find decks in the mtga logs then upload them to my site.
        # bassed off of dirwatcher with an automatic push feature.
        os.chdir("../../../Library/Logs/Wizards Of The Coast/MTGA")
        print(os.listdir())
        with open("""Player.log""", 'r') as f:
            text = f.read()
            decks = []
            match = re.finditer(r'(Exporting deck)[^[{]+', text)
            os.chdir("/Users/marcuschirirboga/coding/q4/magicsite")
            i = 0
            for item in match:
                i += 1
                with open(f"localdecks/decktest{i}.dec", 'w+') as file:
                    deck = item.group(0).strip().split('\n')
                    deck.pop(0)
                    sideboard_index = 0
                    if "Sideboard" in deck:
                        sideboard_index = deck.index("Sideboard")
                        sideboard = deck[sideboard_index:]
                        deck = deck[:sideboard_index]
                    else:
                        sideboard = []
                    deck_dict = dict()
                    sb_dict = {}
                    # handle maindeck
                    for card in deck:
                        if not card:
                            continue
                        if card[0].isalpha():
                            continue
                        quantity = ""
                        while not card[0].isalpha():
                            quantity += card[0]
                            card = card[1:]
                        exact_card = ""
                        while card.find('(') != -1:
                            exact_card = card[-1]+exact_card
                            card = card[:-1]
                        exact_card_number = exact_card[1:4]

                        if "///" in card:
                            card = card.replace("///", "//")
                            print(card)
                        # card_obj = Card.objects.filter(
                        #     set=exact_card[1:4].lower())
                        # card_obj = card_obj.filter(
                        #     collector_number=exact_card[5:].strip()).all()
                        # # print(card_obj)
                        # print(card)
                        # breakpoint()
                        deck_dict.update(
                            {card.strip(): [int(quantity), Card.objects.filter(
                                name__icontains=card.strip()).first().name]})
                    # handle sideboard
                    for card in sideboard:
                        if not card:
                            continue
                        if card[0].isalpha():
                            continue
                        quantity = ""
                        while not card[0].isalpha():
                            quantity += card[0]
                            card = card[1:]
                        exact_card = ""
                        while card.find('(') != -1:
                            exact_card = card[-1]+exact_card
                            card = card[:-1]
                        exact_card_number = exact_card[1:4]

                        if "///" in card:
                            card = card.replace("///", "//")
                            print(card)
                        sb_dict.update({card.strip(): [int(quantity), Card.objects.filter(
                            name__icontains=card.strip()).first().name]})
                    deck_to_save = {"deck": deck_dict, "sideboard": sb_dict}
                    # build deck and query cards.
                    deck_obj = Deck.objects.create(
                        title=f'deck{i}',
                        description='hold',
                        arena_export_list='\n'.join(deck),
                        actual_decklist=deck_to_save,
                        user=User.objects.get(id=1),
                    )
                    for card in deck_obj.actual_decklist['deck'].keys() | deck_obj.actual_decklist['sideboard'].keys():
                        deck_obj.card_obj_in_deck.add(
                            Card.objects.filter(name=card).first())
                        deck_obj.save()
                    legality = []
                    for card in deck_obj.card_obj_in_deck.all():
                        if card.legalities["standard"] == 'not_legal':
                            print(card.name)
                            legality.append("not in standard")
                        if card.legalities["historic"] == "legal":
                            legality.append("historic")
                    if "not in standard" in legality:
                        deck_obj.format = "Historic"
                        deck_obj.save()
                    else:
                        deck_obj.format = 'Standard'
                        deck_obj.save()

                        # put in color parsing

                    print(legality)
                    file.write(str(deck_to_save))
