from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('seasons/', views.get_seasons, name='get_seasons'),
    path('seasons/<int:season>/standings', views.standings, name='standings'),
    path('seasons/<int:season>/races/', views.races, name='season_races'),
    path('circuits/', views.circuits, name='circuits'),
    path('circuits/<str:circuit_id>/races/', views.circuit_races, name='circuit_races'),
    path('race_results/<int:season>/<int:round>/', views.race_results, name='race_results'),
]
