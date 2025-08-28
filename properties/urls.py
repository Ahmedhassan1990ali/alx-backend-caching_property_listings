from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'properties-viewset', views.PropertyViewSet, basename='property')

urlpatterns = [
    # Cache management endpoints
    path('cache-info/', views.cache_info, name='cache-info'),
    path('clear-cache/', views.clear_cache, name='clear-cache'),
    
    # Include router URLs
    path('', include(router.urls)),

    # Traditional Django view 
    path('properties-json/', views.property_list, name='property-list-json'),
]