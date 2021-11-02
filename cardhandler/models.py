from django.db import models
from django.db.models.fields import UUIDField

# A model for my website for magic cards
# TODO: add color for advanced filtering.


class Card(models.Model):
    oracle_id = models.UUIDField()
    arena_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200)
    layout = models.TextField(max_length=20)
    mana_cost = models.CharField(max_length=200, null=True, blank=True)
    type_line = models.CharField(max_length=200, null=True, blank=True)
    set = models.CharField(max_length=200)
    layout = models.CharField(max_length=40)
    collector_number = models.CharField(max_length=200)
    rarity = models.CharField(max_length=20)
    set_name = models.CharField(max_length=200)
    oracle_text = models.TextField(max_length=200, null=True, blank=True)
    image_url_small = models.TextField(max_length=200, null=True, blank=True)
    image_url_normal = models.TextField(max_length=200, null=True, blank=True)
    image_url_art_crop = models.TextField(
        max_length=200, null=True, blank=True)
    alt_image_url_small = models.TextField(
        max_length=200, null=True, blank=True)
    alt_image_url_normal = models.TextField(
        max_length=200, null=True, blank=True)
    alt_image_url_art_crop = models.TextField(
        max_length=200, null=True, blank=True)
    legalities = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

  # {"object":"card",
  # "id":"86bf43b1-8d4e-4759-bb2d-0b2e03ba7012"
  # ,"oracle_id":"0004ebd0-dfd6-4276-b4a6-de0003e94237"
  # ,"multiverse_ids":[15862]
  # ,"mtgo_id":15870
  # ,"mtgo_foil_id":15871,
  # "tcgplayer_id":3094,
  # "cardmarket_id":3081,
  # "name":"Static Orb",
  # "lang":"en",
  # "released_at":"2001-04-11",
  # "uri":"https://api.scryfall.com/cards/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012"
  # ,"scryfall_uri":"https://scryfall.com/card/7ed/319/static-orb?utm_source=api",
  # "layout":"normal",
  # "highres_image":true,
  # "image_status":"highres_scan",
  # "image_uris":{"small":"https://c1.scryfall.com/file/scryfall-cards/small/front/8/6/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012.jpg?1562242171",
  # "normal":"https://c1.scryfall.com/file/scryfall-cards/normal/front/8/6/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012.jpg?1562242171",
  # "large":"https://c1.scryfall.com/file/scryfall-cards/large/front/8/6/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012.jpg?1562242171",
  # "png":"https://c1.scryfall.com/file/scryfall-cards/png/front/8/6/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012.png?1562242171",
  # "art_crop":"https://c1.scryfall.com/file/scryfall-cards/art_crop/front/8/6/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012.jpg?1562242171",
  # "border_crop":"https://c1.scryfall.com/file/scryfall-cards/border_crop/front/8/6/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012.jpg?1562242171"},
  # "mana_cost":"{3}",
  # "cmc":3.0,
  # "type_line":"Artifact",
  # "oracle_text":"As long as Static Orb is untapped, players can't untap more than two permanents during their untap steps.",
  # "colors":[],
  # "color_identity":[],
  # "keywords":[],
  # "legalities":{"standard":"not_legal","future":"not_legal","historic":"not_legal","gladiator":"not_legal","pioneer":"not_legal","modern":"not_legal","legacy":"legal","pauper":"not_legal","vintage":"legal","penny":"not_legal","commander":"legal","brawl":"not_legal","historicbrawl":"not_legal","paupercommander":"not_legal","duel":"legal","oldschool":"not_legal","premodern":"legal"},
  # "games":["paper","mtgo"],
  # "reserved":false,
  # "foil":true,
  # "nonfoil":true,
  # "finishes":["nonfoil","foil"],
  # "oversized":false,
  # "promo":false,
  # "reprint":true,
  # "variation":false,
  # "set_id":"230f38aa-9511-4db8-a3aa-aeddbc3f7bb9",
  # "set":"7ed",
  # "set_name":"Seventh Edition",
  # "set_type":"core",
  # "set_uri":"https://api.scryfall.com/sets/230f38aa-9511-4db8-a3aa-aeddbc3f7bb9",
  # "set_search_uri":"https://api.scryfall.com/cards/search?order=set\u0026q=e%3A7ed\u0026unique=prints",
  # "scryfall_set_uri":"https://scryfall.com/sets/7ed?utm_source=api",
  # "rulings_uri":"https://api.scryfall.com/cards/86bf43b1-8d4e-4759-bb2d-0b2e03ba7012/rulings",
  # "prints_search_uri":"https://api.scryfall.com/cards/search?order=released\u0026q=oracleid%3A0004ebd0-dfd6-4276-b4a6-de0003e94237\u0026unique=prints",
  # "collector_number":"319",
  # "digital":false,"rarity":"rare",
  # "flavor_text":"The warriors fought against the paralyzing waves until even their thoughts froze in place.",
  # "card_back_id":"0aeebaf5-8c7d-4636-9e82-8c27447861f7",
  # "artist":"Terese Nielsen",
  # "artist_ids":["eb55171c-2342-45f4-a503-2d5a75baf752"],
  # "illustration_id":"6f8b3b2c-252f-4f95-b621-712c82be38b5",
  # "border_color":"white",
  # "frame":"1997",
  # "full_art":false,
  # "textless":false,
  # "booster":true,
  # "story_spotlight":false,
  # "edhrec_rank":2280,
  # "prices":{"usd":"23.09","usd_foil":"463.50","usd_etched":null,"eur":"11.15","eur_foil":"69.99","tix":"0.19"},
  # "related_uris":{"gatherer":"https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=15862",
  # "tcgplayer_infinite_articles":"https://infinite.tcgplayer.com/search?contentMode=article\u0026game=magic\u0026partner=scryfall\u0026q=Static+Orb\u0026utm_campaign=affiliate\u0026utm_medium=api\u0026utm_source=scryfall",
  # "tcgplayer_infinite_decks":"https://infinite.tcgplayer.com/search?contentMode=deck\u0026game=magic\u0026partner=scryfall\u0026q=Static+Orb\u0026utm_campaign=affiliate\u0026utm_medium=api\u0026utm_source=scryfall","edhrec":"https://edhrec.com/route/?cc=Static+Orb",
  # "mtgtop8":"https://mtgtop8.com/search?MD_check=1\u0026SB_check=1\u0026cards=Static+Orb"}},
