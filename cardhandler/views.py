from django.shortcuts import render
from cardhandler.models import Card
import json

# Create your views here.


def single_card_view(request, name):
    card = Card.objects.filter(name=name)
    return render(request, 'carddetail.html', {'card': card})


def bootstrap_cards(request):
    cards = Card.objects.all()
    cards.delete()

    with open("oracle-cards-20211007090329.json", "r+") as j:
        card_data = json.load(j)

        # breakpoint()
        # print(card_data[0])
        broken_list = []
        for card_dict in card_data:
            if card_dict.get('arena_id') or 'arena' in card_dict['games']:
                images = card_dict.get("image_uris")
                small_url = ""
                normal_url = ""
                art_crop_url = ""

                alt_small_url = ""
                alt_normal_url = ""
                alt_art_crop_url = ""
                if images:
                    images = dict(images)
                if images:
                    small_url = images.get("small")
                    normal_url = images.get("normal")
                    art_crop_url = images.get("art_crop")

                if card_dict.get('layout') == "modal_dfc":
                    card_dict['name'] = card_dict.get('card_faces')[
                        0].get('name')
                    images = card_dict.get('card_faces')[0].get(
                        'image_uris')
                    if images:
                        small_url = images.get("small")
                        normal_url = images.get("normal")
                        art_crop_url = images.get("art_crop")
                    alt_images = card_dict.get('card_faces')[1].get(
                        'image_uris')
                    if alt_images:
                        alt_small_url = alt_images.get("small")
                        alt_normal_url = alt_images.get("normal")
                        alt_art_crop_url = alt_images.get("art_crop")
                print(card_dict["set"], card_dict['collector_number'])
                Card.objects.create(
                    name=card_dict.get("name"),
                    mana_cost=card_dict.get("mana_cost"),
                    type_line=card_dict.get("type_line"),
                    layout=card_dict.get('layout'),
                    set=card_dict.get("set"),
                    collector_number=card_dict.get('collector_number'),
                    set_name=card_dict.get("set_name"),
                    oracle_id=card_dict.get("oracle_id"),
                    arena_id=card_dict.get("arena_id"),
                    oracle_text=card_dict.get("oracle_text"),
                    image_url_small=small_url,
                    image_url_normal=normal_url,
                    image_url_art_crop=art_crop_url,
                    alt_image_url_small=alt_small_url,
                    alt_image_url_normal=alt_normal_url,
                    alt_image_url_art_crop=alt_art_crop_url,
                    legalities=card_dict.get('legalities')
                )
