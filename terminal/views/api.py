"""
API endpoints for partial page updates.
These endpoints return JSON data for real-time queue display updates.
"""

from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from terminal.services import QueueService, TransactionService


@require_GET
@never_cache
def public_queue_api(request):
    """
    API endpoint for public queue display partial updates.
    Returns JSON with all queue entries (queued, boarding, departed).
    
    Query params:
        - route: Optional route ID to filter by
    """
    route_filter = request.GET.get("route")
    if route_filter and route_filter != "all":
        try:
            route_filter = int(route_filter)
        except (ValueError, TypeError):
            route_filter = None
    else:
        route_filter = None

    queue_state = QueueService.get_queue_state(route_filter=route_filter)
    
    return JsonResponse(queue_state)


@require_GET
@never_cache
def tv_display_api(request):
    """
    API endpoint for TV display partial updates.
    Returns JSON with boarding/departed entries and queued count badge.
    
    Query params:
        - route: Optional route ID to filter by
    """
    route_filter = request.GET.get("route")
    if route_filter and route_filter != "all":
        try:
            route_filter = int(route_filter)
        except (ValueError, TypeError):
            route_filter = None
    else:
        route_filter = None

    tv_state = QueueService.get_tv_display_state(route_filter=route_filter)
    
    return JsonResponse(tv_state)


@require_GET
@never_cache
def queue_settings_api(request):
    """
    API endpoint to get current queue display settings.
    Used by frontend to configure refresh intervals and countdown durations.
    """
    settings = QueueService.get_settings()
    
    return JsonResponse({
        "refresh_interval": QueueService.get_refresh_interval(),
        "countdown_duration": QueueService.get_countdown_duration(),
        "departure_duration_minutes": QueueService.get_departure_duration(),
    })
