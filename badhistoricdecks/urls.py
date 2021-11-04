from django.urls import path
from badhistoricdecks import views
from cardhandler.views import single_card_view, bootstrap_cards
urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:user_id>/', views.user_detail),
    path('decks/edit/<int:deck_id>/', views.deck_edit),
    path('decks/<int:deck_id>/', views.decklist_detail),
    path('decks/<int:deck_id>/delete', views.decklist_delete_view),
    path('signup/', views.SignUp.as_view()),
    path('upload/', views.DeckFormView.as_view()),
    path('card/<str:name>/', single_card_view),
    path("bootstrap_cards/", bootstrap_cards),

    path('alltags/', views.all_tags_view, name="all_tags"),
    path('tag/<str:tag_slug>/', views.single_tag_view),
    path('addtags/<int:deck_id>/', views.add_tag),
    path('deletetag/<str:tag>/<int:deck_id>', views.delete_tag)
]
