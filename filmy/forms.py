from django.forms import ModelForm
from .models import Film, DodatkoweInfo, Ocena, Aktor

class FilmForm(ModelForm):
    class Meta:
        model = Film
        fields = ['tytul', 'opis', 'premiera', 'rok', 'imdb_rating', 'plakat']


class DodatkoweInfoForm(ModelForm):
    class Meta:
        model = DodatkoweInfo
        fields = ['czas_trwania', 'gatunek']

class OcenaForm(ModelForm):
    class Meta:
        model = Ocena
        fields = ['gwiazdki', 'recenzja']

class AktorForm(ModelForm):
    class Meta:
        model = Aktor
        fields = ['imie', 'nazwisko']