from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q

from terminal.models import EntryLog
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
    now = timezone.now()
    now, departure_duration, departed_cutoff = maintenance_task(now=now)

    route_filter = request.GET.get('route')

    queue_logs = (
        EntryLog.objects
        .select_related('vehicle', 'vehicle__assigned_driver', 'vehicle__route')
        .filter(
            status=EntryLog.STATUS_SUCCESS
        )
        .filter(
            Q(is_active=True) | Q(departed_at__gte=departed_cutoff)
        )
        .order_by('created_at')
    )

    if route_filter and route_filter != 'all':
        queue_logs = queue_logs.filter(vehicle__route_id=route_filter)

    entries = build_public_queue_entries(queue_logs, now, departure_duration, departed_cutoff)

    routes = Route.objects.filter(active=True).order_by("origin", "destination")

    context = {
        "queue_entries": entries,
        "routes": routes,
        "selected_route": route_filter,
        "departure_duration_minutes": departure_duration,
        "server_now": timezone.localtime(now),
    }

    return render(request, 'passenger/public_queue.html', context)


def public_queue_data(request):
    now = timezone.now()
    now, departure_duration, departed_cutoff = maintenance_task(now=now)

    route_filter = request.GET.get("route", "all")

    queue_logs = (
        EntryLog.objects
        .select_related("vehicle", "vehicle__assigned_driver", "vehicle__route")
        .filter(
            status=EntryLog.STATUS_SUCCESS
        )
        .filter(
            Q(is_active=True) | Q(departed_at__gte=departed_cutoff)
        )
        .order_by("created_at")
    )

    if route_filter and route_filter != "all":
        queue_logs = queue_logs.filter(vehicle__route_id=route_filter)

    entries = build_public_queue_entries(queue_logs, now, departure_duration, departed_cutoff)

    return JsonResponse({
        "entries": entries,
        "server_time": int(now.timestamp()),
    })
