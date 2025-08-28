from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from .models import Property
import time

# Create your views here.
def property_list(request):
    cache_key = 'all_properties'
    
    # Try to get data from cache
    properties = cache.get(cache_key)
    
    if properties is None:
        # If not in cache, query database and cache the result
        properties = list(Property.objects.values('id', 'title', 'price', 'location', 'created_at'))
        cache.set(cache_key, properties, timeout=60 * 60)  # Cache for 1 hour
        source = 'database'
    else:
        source = 'cache'
    
    return JsonResponse({
        'properties': properties,
        'source': source,
        'count': len(properties)
    })

def clear_cache(request):
    cache.clear()
    return JsonResponse({'message': 'Cache cleared successfully'})