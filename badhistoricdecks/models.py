from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from cardhandler.models import Card
# Create your models here.
"""user model:

Name (CharField)
email (TextField)
deck Model:

Title (CharField)
Author (ForeignKey)
Description (TextField)
Instructions (TextField)"""


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.username} : {self.email}"


class Deck(models.Model):
    format_choices = [
        ('Historic', 'Historic'),
        ('Standard', 'Standard')
    ]

    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=50)
    description = models.TextField()
    arena_export_list = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="builder")
    actual_decklist = models.JSONField(
        null=True, blank=True)
    format = models.CharField(max_length=40, choices=format_choices)
    card_obj_in_deck = models.ManyToManyField(
        Card, related_name='card_obj_in_deck', symmetrical=False, blank=True)
    card_highlights = models.ManyToManyField(
        Card, related_name='card_highlights', symmetrical=False, blank=True)
    deck_tags = models.ManyToManyField('Tags', related_name="tags")

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Tags(models.Model):
    tag = models.SlugField(max_length=48, null=False, unique=True)

    def __str__(self):
        return f"{self.tag}"
