from mtgsdk import Card, Set

cards = Card.where(set='ons').all()
for card in cards:
    print(card.image_url)
set = Set.where(name='onslaught').all()
for i in set[0]:
    print(i.name)
