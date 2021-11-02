from django.contrib import admin

from badhistoricdecks.models import Tags, User, Deck
admin.site.register(User)
admin.site.register(Deck)
admin.site.register(Tags)
