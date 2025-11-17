"""
Custom middleware for HTTP caching headers and rate limiting
"""
from django.utils.cache import add_never_cache_headers, patch_cache_control
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from datetime import timedelta


class APICacheMiddleware:
    """
    Middleware to add cache-control headers to API responses.
    - All API requests are set to no-cache for immediate updates
    - This ensures data changes in admin panel are reflected immediately on frontend
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Add no-cache headers to all API endpoints for immediate updates
        if request.path.startswith('/api/'):
            add_never_cache_headers(response)

        return response


class RateLimitMiddleware:
    """
    Middleware to implement rate limiting based on configurable settings.
    Tracks both per-route and total request limits.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        """Extract client IP from request, considering proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def __call__(self, request):
        # Import here to avoid circular imports
        from api.models import RateLimitSettings, RateLimitLog

        # Get rate limit settings
        try:
            settings = RateLimitSettings.get_settings()
        except Exception:
            # If settings don't exist or there's an error, allow the request
            return self.get_response(request)

        # Skip rate limiting if disabled
        if not settings.enabled:
            return self.get_response(request)

        # Get client IP
        ip_address = self.get_client_ip(request)
        if not ip_address:
            return self.get_response(request)

        # Skip rate limiting for admin users
        if request.user and request.user.is_staff:
            return self.get_response(request)

        # Get current route
        route = request.path

        # Calculate time window
        time_window = timezone.now() - timedelta(hours=float(settings.time_window_hours))

        # Check if IP is currently blocked
        try:
            # Check for active blocks across any route
            active_blocks = RateLimitLog.objects.filter(
                ip_address=ip_address,
                is_blocked=True,
                blocked_until__gt=timezone.now()
            )

            if active_blocks.exists():
                blocked_until = active_blocks.first().blocked_until
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'You have been temporarily blocked due to excessive requests. Please try again later.',
                    'blocked_until': blocked_until.isoformat(),
                    'status': 429
                }, status=429)

            # Get or create log entry for this IP + route
            log_entry, created = RateLimitLog.objects.get_or_create(
                ip_address=ip_address,
                route=route,
                defaults={'request_count': 0}
            )

            # Reset count if outside time window
            if not created and log_entry.last_request_at <= time_window:
                log_entry.request_count = 0
                log_entry.save()

            # Increment request count
            log_entry.request_count += 1
            log_entry.save()

            # Check per-route limit
            if log_entry.request_count > settings.max_requests_per_route:
                self._block_ip(log_entry, settings)
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests to this route. Maximum {settings.max_requests_per_route} requests per {settings.time_window_hours} hour(s).',
                    'status': 429
                }, status=429)

            # Check total requests across all routes
            total_requests = RateLimitLog.objects.filter(
                ip_address=ip_address,
                last_request_at__gte=time_window
            ).aggregate(total=models.Sum('request_count'))['total'] or 0

            if total_requests > settings.max_total_requests:
                self._block_ip(log_entry, settings)
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many total requests. Maximum {settings.max_total_requests} requests across all routes per {settings.time_window_hours} hour(s).',
                    'status': 429
                }, status=429)

        except Exception as e:
            # If there's any error with rate limiting, allow the request
            # (fail open instead of fail closed)
            print(f"Rate limiting error: {e}")
            pass

        return self.get_response(request)

    def _block_ip(self, log_entry, settings):
        """Block an IP address for the configured duration."""
        log_entry.is_blocked = True
        log_entry.blocked_at = timezone.now()
        log_entry.blocked_until = timezone.now() + timedelta(hours=float(settings.block_duration_hours))
        log_entry.save()
