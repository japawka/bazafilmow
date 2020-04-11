"""bazafilmow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from filmy.views import register, wszystkie_filmy
from rest_framework import routers
from filmy.views import UserView, FilmView

router = routers.DefaultRouter()
router.register(r'users', UserView)
router.register(r'filmy', FilmView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filmy/', include('filmy.urls')),
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('', wszystkie_filmy, name="wszystkie_filmy"),
    path('register/', register, name="register")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
