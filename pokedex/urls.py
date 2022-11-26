from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>', views.index, name='index'),
    path('pokedex/<int:pokemon_id>/', views.detail, name='detail'),
    path('teams', views.teams, name='teams')
]