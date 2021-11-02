from django.shortcuts import render
from cardhandler.models import Card
# Create your views here.


def single_card_view(request, name):
    card = Card.objects.filter(name=name)
    return render(request, 'carddetail.html', {'card': card})
