from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.property_list, name='property_list'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
]