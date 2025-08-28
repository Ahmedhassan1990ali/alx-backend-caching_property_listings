from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Function to get all properties with low-level caching
    Checks Redis for cached data, fetches from database if not found
    Caches the queryset for 1 hour (3600 seconds)
    """
    # Check if data is in cache
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        # Return cached data
        return cached_properties
    
    # If not in cache, fetch from database
    queryset = Property.objects.all()
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set('all_properties', queryset, 3600)
    
    return queryset