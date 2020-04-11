from django.urls import path
from . import views

urlpatterns = [
    path('wszystkie/', views.wszystkie_filmy, name="wszystkie_filmy"),
    path('nowy/', views.nowy_film, name="nowy_film"),
    path('edit/<int:id>/', views.edytuj_film, name="edytuj_film"),
    path('delete/<int:id>/', views.delete_film, name="usun_film"),
    path('detail/<int:id>/', views.film_detail, name="detail"),
]
