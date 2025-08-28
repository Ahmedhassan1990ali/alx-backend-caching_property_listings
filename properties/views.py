from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer
import time

# Create your views here.
# Class-based view with cache 
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# Utility view to check cache status
@api_view(['GET'])
def cache_info(request):
    """
    View to check cache status and statistics
    """
    cache_stats = cache._cache.get_client().info()
    cache_keys = cache._cache.get_client().keys('*')
    
    return Response({
        'cache_stats': cache_stats,
        'cache_keys': [key.decode('utf-8') for key in cache_keys],
        'cache_ttl': '15 minutes for property listings'
    })

# View to clear cache
@api_view(['POST'])
def clear_cache(request):
    """
    View to clear the entire cache
    """
    cache.clear()
    return Response({'message': 'Cache cleared successfully'})

# Traditional Django view without DRF
@cache_page(60 * 15)
def property_list(request):
    """
    Traditional Django view returning JsonResponse
    """
    properties = Property.objects.all().values('id', 'title', 'description', 'price', 'location', 'created_at')
    data = {
        'properties': list(properties),
        'count': len(properties),
        'timestamp': time.time()
    }
    return JsonResponse({
        'properties': list(properties),
        'count': len(properties),
        'timestamp': time.time()
    })