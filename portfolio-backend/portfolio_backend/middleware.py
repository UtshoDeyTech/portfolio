"""
Custom middleware for adding HTTP caching headers to API responses
"""
from django.utils.cache import add_never_cache_headers, patch_cache_control


class APICacheMiddleware:
    """
    Middleware to add cache-control headers to API responses for better performance.
    - GET requests to /api/ endpoints get cached for 5 minutes
    - Other methods (POST, PUT, DELETE) are never cached
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only add caching to API endpoints
        if request.path.startswith('/api/'):
            # Only cache GET requests
            if request.method == 'GET':
                # Cache for 5 minutes (300 seconds)
                # public = can be cached by browsers and CDNs
                # max-age = how long to cache
                # stale-while-revalidate = serve stale content while fetching fresh
                patch_cache_control(
                    response,
                    public=True,
                    max_age=300,  # 5 minutes
                    stale_while_revalidate=60  # 1 minute grace period
                )
            else:
                # Don't cache POST, PUT, DELETE, etc.
                add_never_cache_headers(response)

        return response
