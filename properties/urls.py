from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'properties-viewset', views.PropertyViewSet, basename='property')

urlpatterns = [
    path('properties/', views.property_list, name='property-list'),
    path('cache-info/', views.cache_info, name='cache-info'),
    path('clear-cache/', views.clear_cache, name='clear-cache'),
]