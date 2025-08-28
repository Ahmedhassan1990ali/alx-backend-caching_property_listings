from django.core.cache import cache
from django_redis import get_redis_connection
import logging
from .models import Property

# Set up logger
logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics
    Connects to Redis via django_redis, gets keyspace metrics
    Calculates hit ratio and returns comprehensive metrics dictionary
    """
    try:
        # Get Redis connection
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO command output
        info = redis_conn.info()
        
        # Extract cache statistics
        stats = info.get('stats', {})
        keyspace_hits = stats.get('keyspace_hits', 0)
        keyspace_misses = stats.get('keyspace_misses', 0)
        
        # Calculate hit ratio (avoid division by zero)
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0
        
        # Get memory usage
        memory_used = info.get('used_memory', 0)
        memory_used_human = info.get('used_memory_human', '0B')
        
        # Get key count
        db_info = info.get('db0', {})
        key_count = db_info.get('keys', 0)
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 4),
            'hit_ratio_percentage': round(hit_ratio * 100, 2),
            'memory_used_bytes': memory_used,
            'memory_used_human': memory_used_human,
            'key_count': key_count,
            'uptime_seconds': info.get('uptime_in_seconds', 0),
            'connected_clients': info.get('connected_clients', 0),
            'status': 'success'
        }
        
        # Log the metrics
        logger.info(
            f"Redis Cache Metrics - Hits: {keyspace_hits}, Misses: {keyspace_misses}, "
            f"Hit Ratio: {hit_ratio:.2%}, Keys: {key_count}, Memory: {memory_used_human}"
        )
        
        return metrics
        
    except Exception as e:
        # Log error and return error metrics
        error_message = f"Error retrieving Redis metrics: {str(e)}"
        logger.error(error_message)
        
        return {
            'status': 'error',
            'error_message': error_message,
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_operations': 0,
            'hit_ratio': 0,
            'hit_ratio_percentage': 0,
            'memory_used_bytes': 0,
            'memory_used_human': '0B',
            'key_count': 0,
            'uptime_seconds': 0,
            'connected_clients': 0
        }