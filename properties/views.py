from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties, get_redis_cache_metrics
from .models import Property
import time

# Create your views here.
# Traditional Django view without DRF
@cache_page(60 * 15)
def property_list(request):
    """
    View to list all properties using low-level cached queryset
    """
    # Use the utility function to get properties (cached for 1 hour)
    properties = get_all_properties()
    
    # Convert queryset to list of dictionaries for JSON response
    properties_data = list(properties.values('id', 'title', 'description', 'price', 'location', 'created_at'))

    return JsonResponse({
        'properties': properties_data,
        'count': len(properties_data),
        'cache_info': 'View response cached for 15 minutes, queryset cached for 1 hour',
        'timestamp': time.time()
    })

def cache_info(request):
    """
    View to show cache information
    """
    # Check if all_properties key exists in cache
    has_cached_properties = cache.has_key('all_properties')
    cache_ttl = cache.ttl('all_properties') if has_cached_properties else None
    
    return JsonResponse({
        'all_properties_cached': has_cached_properties,
        'cache_ttl_seconds': cache_ttl,
        'cache_ttl_minutes': cache_ttl / 60 if cache_ttl else None,
        'message': 'Queryset is cached for 1 hour (3600 seconds)'
    })

def clear_cache(request):
    """
    View to clear the cache
    """
    cache.delete('all_properties')
    return JsonResponse({'message': 'Cache cleared successfully'})

def cache_metrics(request):
    """
    View to display Redis cache metrics
    """
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)
