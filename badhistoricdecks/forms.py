from django import forms
from django.forms.widgets import Textarea
from badhistoricdecks.models import Deck


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class DeckForm(forms.Form):
    title = forms.CharField(max_length=50)
    decklist = forms.CharField(widget=Textarea)
    description = forms.CharField(widget=Textarea)
    actual_decklist = forms.CharField(
        initial="json field")

    # id = models.AutoField(primary_key=True)

    # title = models.CharField(max_length=50, )
    # decklist = models.TextField()
    # description = models.TextField()
    # publish_date = models.DateTimeField(default=timezone.now)
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="builder")


# class DeckEditForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     decklist = forms.CharField(widget=Textarea)
#     description = forms.CharField(widget=Textarea)
#     actual_decklist = forms.JSONField(initial="json field")


class DeckEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DeckEditForm, self).__init__(*args, **kwargs)
        self.fields['format'].widget.attrs['class'] = 'browser-default'

    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=Textarea)
    format = forms.ChoiceField(choices=Deck.format_choices)

    # def save(self, commit=True):
    # return super(PointForm, self).save(commit=commit)


class AddTagForm(forms.Form):
    tag = forms.SlugField()
