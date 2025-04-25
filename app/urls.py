from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('seasons/', views.get_seasons, name='get_seasons'),
    path('seasons/<int:season>/', views.standings, name='standings'),
    path('circuits/', views.circuits, name='circuits'),
]
