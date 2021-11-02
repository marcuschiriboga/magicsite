from django.shortcuts import redirect, render
from badhistoricdecks.models import User, Deck, Tags
from badhistoricdecks.forms import AddTagForm, DeckEditForm, SignUpForm, DeckForm
from django.views import View
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from cardhandler.models import Card


def index(request):
    decks = Deck.objects.all()
    if request.GET.get:
        print(request.GET)
        # if "colors" in request.GET:
        #     decks = decks.filter(colors__in=request.GET.get("colors"))
        if "format" in request.GET:
            if not request.GET.get("format") == "all":
                decks = decks.filter(format=request.GET.get("format"))
        if "tags" in request.GET:
            decks = decks.filter(
                deck_tags__tag=request.GET.get("tags"))

    print(decks)
    context = {
        "decks": decks,
        "tags": Tags.objects.all()
    }
    return render(request, 'index.html', context)


def decklist_detail(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    cards = []
    # for card in deck.actual_decklist['deck'].keys():
    #     try:
    #         one_card = Card.objects.filter(name__icontains=card).first()
    #         cards.append(one_card)
    #     except:
    #         cards.append(card)
    # refactor to use the built it many to many
    return render(request, "decklist_detail.html", {"deck": deck, 'cards': "cards"})


def decklist_delete_view(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    deck.delete()
    return HttpResponseRedirect("/")


def user_detail(request, user_id):
    decks = Deck.objects.filter(user_id=user_id)
    print(decks)
    return render(
        request, "user_detail.html", {
            "decks": decks}
    )


class SignUp(View):

    form_class = SignUpForm

    def get(self, request):
        html = 'generic_form.html'
        form = self.form_class
        context = {'form': form}
        return render(request, html, context)

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create(
                username=data['username'],
                password=data['password'],
            )
            return HttpResponseRedirect(reverse('Login'))

# TODO: absract get_deck logic to be reusable elsewhere


class DeckFormView(View):

    form_class = DeckForm

    def get(self, request):
        html = 'generic_form.html'
        form = self.form_class
        context = {'form': form}
        return render(request, html, context)

    def post(self, request):

        # refactor out hack code
        if request.method == 'POST':
            form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            deck = data["decklist"].strip().split('\r\n')
            deck.pop(0)
            print(deck)
            sideboard_index = -1
            if "sideboard" in deck:
                sideboard_index = deck.index("sideboard")
            sideboard = deck[sideboard_index:]
            deck = deck[:sideboard_index]
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
                quantity = card[0]
                if quantity.isalpha():
                    continue
                while not card[0].isalpha():
                    card = card[1:]
                while card.find('(') != -1:
                    card = card[: -1]
                sb_dict.update({card.strip(): [int(quantity), Card.objects.filter(
                    name__icontains=card.strip()).first().name]})
            deck_to_save = {"deck": deck_dict, "sideboard": sb_dict}
            # build deck and query cards.
            deck_obj = Deck.objects.create(
                title=data["title"],
                description=data["description"],
                arena_export_list='\n'.join(deck),
                actual_decklist=deck_to_save,
                user=User.objects.get(id=1),
            )
            for card in deck_obj.actual_decklist['deck'].keys() | deck_obj.actual_decklist['sideboard'].keys():
                deck_obj.card_obj_in_deck.add(
                    Card.objects.filter(name__icontains=card).first())
                deck_obj.save()
            legality = []
            # incomplete legality filtering
            for card in deck_obj.card_obj_in_deck.all():
                if card.legalities["standard"] == 'not_legal':
                    print(card.name)
                    legality.append("not in standard")
                if card.legalities["historic"] == "legal":
                    legality.append("historic")
            print(data['actual_decklist'])
            return redirect('/decks/'+str(deck_obj.id))


class search_view(View):
    model = Deck
    template_name = 'search_results.html'

    def get(self, request):
        o = request.GET.getlist("o")

        if not request.GET.get('o'):
            o = ['cards', 'decks', 'tags']
        if type(o) == str:
            o = [o]

        card_list, deck_list, tag_list = list(), list(), list()
        query = self.request.GET.get('q')
        print(o, query)
        if "cards" in o:
            card_list = Card.objects.filter(
                Q(name__icontains=query) | Q(oracle_text__icontains=query)).distinct()
        if "decks" in o:
            deck_list = Deck.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(actual_decklist__icontains=query) |
                Q(deck_tags__tag__icontains=query) |
                Q(format__icontains=query)
            ).distinct()
        if "tags" in o:
            tag_list = Tags.objects.filter(tag__icontains=query).distinct()
        object_list = list(deck_list)+list(card_list)+list(tag_list)
        return render(request, self.template_name, {'object_list': object_list, 'query': query})


def static_view(request):
    return render(request, 'statictodo.html')


def all_tags_view(request):
    tags = Tags.objects.all()
    if request.GET.get("filter_q"):
        filter_q = request.GET.get("filter_q")
        tags = tags.filter(Q(tag__icontains=filter_q)).all()
    tags = sorted(tags, key=lambda x: x.tags.count())[::-1]
    return render(request, 'all_tags.html', {"tags": tags})


def single_tag_view(request, tag_slug):
    tag = Tags.objects.filter(tag=tag_slug).first()
    return render(request, 'single_tag.html', {"tag": tag})


def add_tag(request, deck_id):
    if request.method == 'POST':
        print("yay")
        form = AddTagForm(request.POST)

        if form.is_valid():
            form = form.cleaned_data
            try:
                tag = Tags.objects.get(tag=form["tag"])
                deck = Deck.objects.get(id=deck_id)
                deck.deck_tags.add(tag)
                deck.save()
                print('works?')
                # deck . add tag
            except:
                tag = Tags.objects.create(tag=form['tag'])
                deck = Deck.objects.get(id=deck_id)
                deck.deck_tags.add(tag)
                deck.save()
                print('works?')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_tag(request, tag, deck_id):
    tag_ = Tags.objects.get(tag=tag)
    deck = Deck.objects.get(id=deck_id)
    deck.deck_tags.remove(tag_)
    deck.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deck_edit(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    form = DeckEditForm(
        initial={"title": deck.title, 'description': deck.description, "format": deck.format})
    if request.user == deck.user:
        print("they are the same")
    else:
        print("they are different")
        return HttpResponseRedirect('/')
    if request.method == "POST":
        form_returned = DeckEditForm(request.POST)
        if form_returned.is_valid():
            deck.title = request.POST["title"]
            deck.description = request.POST['description']
            deck.format = request.POST["format"]
            deck.save()
        return HttpResponseRedirect(f"/decks/{deck_id}/")
    return render(request, "deck_edit.html", {"deck": deck, "form": form})
