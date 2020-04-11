from django.shortcuts import render, get_object_or_404, redirect
from .models import Film, DodatkoweInfo, Ocena, Aktor
from .forms import FilmForm, DodatkoweInfoForm, OcenaForm, AktorForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import os
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer, FilmSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FilmView(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer



def wszystkie_filmy(request):
    wszystkie = Film.objects.all()
    return render(request, 'filmy.html', {'filmy': wszystkie})

@login_required
def nowy_film(request):
    form_film = FilmForm(request.POST or None, request.FILES or None)
    form_dodatkowe = DodatkoweInfoForm(request.POST or None)
    if all((form_film.is_valid(), form_dodatkowe.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowe.save()
        film.dodatkowe = dodatkowe
        form_film.save()
        return redirect(wszystkie_filmy)
    context = {
        'form': form_film,
        'form_dodatkowe': form_dodatkowe,
        'oceny': None,
        'form_ocena': None,
        'nowy': True,
        'actor_form': None
    }
    return render(request, 'film_form.html', context)

@login_required
def edytuj_film(request, id):
    film = get_object_or_404(Film, pk=id)
    oceny = Ocena.objects.filter(film=film)

    try:
        dodatkowe = DodatkoweInfo.objects.get(film=film.id)
    except DodatkoweInfo.DoesNotExist:
        dodatkowe = None

    form_film = FilmForm(request.POST or None, request.FILES or None, instance=film)
    form_dodatkowe = DodatkoweInfoForm(request.POST or None, instance=dodatkowe)
    form_ocena = OcenaForm(None)
    actor_form = AktorForm(request.POST or None)
    if request.method == 'POST':
        if 'gwiazdki' in request.POST:
            ocena = form_ocena.save(commit=False)
            ocena.film = film
            ocena.save()

    if all((form_film.is_valid(), form_dodatkowe.is_valid())):
        film = form_film.save(commit=False)
        dodatkowe = form_dodatkowe.save()
        film.dodatkowe = dodatkowe
        film.save()
        return redirect(wszystkie_filmy)


    if request.method == "POST":
        if 'imie' in request.POST:
            actor = actor_form.save()
            actor.filmy.add(film)
            return redirect(wszystkie_filmy)

    context = {
        'form': form_film,
        'form_dodatkowe': form_dodatkowe,
        'oceny': oceny,
        'form_ocena': form_ocena,
        'nowy': False,
        'actor_form': actor_form,

    }

    return render(request, 'film_form.html', context)

@login_required
def delete_film(request, id):
    film = get_object_or_404(Film, pk=id)

    if request.method == "POST":
        film.delete()
        if film.plakat:
            if os.path.isfile(film.plakat.path):
                os.remove(film.plakat.path)
        return redirect(wszystkie_filmy)

    return render(request, 'potwierdz.html', {'film': film})


def film_detail(request, id):
    film = get_object_or_404(Film, pk=id)
    actors = film.aktorzy.all()
    oceny = Ocena.objects.filter(film=film)
    ocena_form = OcenaForm(request.POST or None)

    if request.method == "POST":
        if 'stars' in request.POST:
            ocena = ocena_form.save(commit=False)
            ocena.film = film
            ocena.save()
            return redirect(wszystkie_filmy)

    context = {
        'film': film,
        'oceny': oceny,
        'ocena_form': ocena_form,
        'actors': actors
    }
    return render(request, 'film_detail.html', context)

def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(wszystkie_filmy)
    return render(request, 'register.html', {'form': form})