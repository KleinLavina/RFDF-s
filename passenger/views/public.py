import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

from terminal.models import EntryLog
from terminal.services import QueueService
from terminal.shared_queue import build_public_queue_entries
from terminal.views.shared import maintenance_task
from vehicles.models import Route


def home(request):
    return render(request, 'passenger/home.html')


def announcement(request):
    return render(request, 'passenger/announcement.html')


def contact(request):
    return render(request, 'passenger/contact.html')


def public_queue_view(request):
    """
    Public queue view with partial page update support.
    Initial load renders template, subsequent updates via WebSocket/fetch.
    """
    route_filter = request.GET.get('route')
    route_id = None

    if route_filter and route_filter != 'all':
        try:
            route_id = int(route_filter)
        except (ValueError, TypeError):
            route_id = None

    # Get queue state from service layer
    queue_state = QueueService.get_queue_state(route_filter=route_id)

    routes = Route.objects.filter(active=True).order_by("origin", "destination")

    context = {
        "queue_entries": json.dumps(queue_state.get("entries", [])),
        "routes": routes,
        "selected_route": route_filter,
        "departure_duration_minutes": queue_state.get("departure_duration_minutes", 30),
        "server_now": timezone.localtime(timezone.now()),
        "countdown_duration": queue_state.get("countdown_duration", 30),
        "refresh_interval": queue_state.get("refresh_interval", 15),
    }

    return render(request, 'passenger/public_queue.html', context)


def public_queue_data(request):
    """
    API endpoint for queue data updates.
    Returns JSON with all queue entries for partial DOM updates.
    """
    route_filter = request.GET.get("route", "all")
    route_id = None

    if route_filter and route_filter != "all":
        try:
            route_id = int(route_filter)
        except (ValueError, TypeError):
            route_id = None

    queue_state = QueueService.get_queue_state(route_filter=route_id)

    return JsonResponse(queue_state)
