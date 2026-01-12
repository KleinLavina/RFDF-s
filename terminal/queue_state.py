from collections import OrderedDict
from datetime import timedelta

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from terminal.models import EntryLog, SystemSettings
from vehicles.models import QueueHistory

DEPARTED_VISIBLE_SECONDS = 30
DEPARTED_COUNTDOWN_SECONDS = DEPARTED_VISIBLE_SECONDS
HISTORY_LIMIT_PER_ROUTE = 3


def finalize_departure(entry_log, now=None):
    """
    Atomically mark an entry log as departed, trigger the 30s departed visibility window,
    and keep the record visible for the centralized countdown logic.
    """
    if not entry_log or not entry_log.is_active:
        return entry_log

    now = now or timezone.now()
    with transaction.atomic():
        entry_log.is_active = False
        entry_log.departed_at = now
        entry_log.save(update_fields=["is_active", "departed_at"])

    return entry_log


def run_queue_housekeeping(now=None, delete_after_minutes=None):
    """
    Centralized maintenance helper that closes overdue entries and trims old records.
    """
    now = now or timezone.now()
    settings = SystemSettings.get_solo()
    departure_duration = getattr(settings, "departure_duration_minutes", 30)

    cutoff = now - timedelta(minutes=int(departure_duration))
    stale_entries = EntryLog.objects.filter(is_active=True, created_at__lte=cutoff)
    for log in stale_entries:
        finalize_departure(log, now=now)

    if delete_after_minutes is not None:
        delete_cutoff = now - timedelta(minutes=int(delete_after_minutes))
        EntryLog.objects.filter(created_at__lt=delete_cutoff).delete()


def _format_log_entry(
    log,
    status,
    departure_duration,
    route_name,
    now,
    route_id=None,
    persist_boarding_start=False,
):
    vehicle = getattr(log, "vehicle", None)
    driver = getattr(vehicle, "assigned_driver", None) if vehicle else None
    boarding_start = log.boarding_started_at or now
    expiry_timestamp = None

    if status == "Boarding":
        if persist_boarding_start and not log.boarding_started_at:
            EntryLog.objects.filter(pk=log.pk).update(boarding_started_at=boarding_start)
        expiry = boarding_start + timedelta(minutes=departure_duration)
        expiry_timestamp = int(expiry.timestamp())

    entry_display = timezone.localtime(log.created_at).strftime("%b %d, %Y %I:%M %p")
    entry_numeric = entry_display
    departure_time = log.created_at + timedelta(minutes=departure_duration)
    departure_display = timezone.localtime(departure_time).strftime("%b %d, %Y %I:%M %p")

    return {
        "id": log.id,
        "entry_time_display": entry_display,
        "entry_time_numeric": entry_numeric,
        "departure_time_display": departure_display,
        "vehicle_plate": vehicle.license_plate if vehicle else "—",
        "route": route_name,
        "route_id": route_id,
        "driver_name": f"{driver.first_name} {driver.last_name}" if driver else "N/A",
        "status": status,
        "countdown_active": status == "Boarding",
        "expiry_timestamp": expiry_timestamp,
        "departed_countdown_active": False,
        "departed_countdown_expiry": None,
    }


def _build_route_entries(route_name, route_id, logs, now, departure_duration, departed_cutoff, countdown_seconds, persist_boarding_start=False):
    entries = []
    active_logs = [log for log in logs if log.is_active]
    departed_logs = [
        log for log in logs if log.departed_at and log.departed_at >= departed_cutoff
    ]

    active_logs.sort(key=lambda log: log.created_at)
    departed_logs.sort(key=lambda log: log.departed_at)

    cooldown_log = None
    cooldown_expiry = None
    if departed_logs:
        latest_departed = departed_logs[-1]
        expiry = latest_departed.departed_at + timedelta(seconds=countdown_seconds)
        if expiry > now:
            cooldown_log = latest_departed
            cooldown_expiry = expiry

    boarding_log = active_logs[0] if active_logs and not cooldown_log else None

    for log in active_logs:
        status = "Boarding" if log == boarding_log else "Queued"
        entry = _format_log_entry(
            log,
            status,
            departure_duration,
            route_name,
            now,
            route_id=route_id,
            persist_boarding_start=persist_boarding_start,
        )
        entries.append(entry)

    if cooldown_log:
        vehicle = getattr(cooldown_log, "vehicle", None)
        driver = getattr(vehicle, "assigned_driver", None) if vehicle else None
        entry = _format_log_entry(
            cooldown_log,
            "Departed",
            departure_duration,
            route_name,
            now,
            route_id=route_id,
            persist_boarding_start=persist_boarding_start,
        )
        entry.update({
            "countdown_active": False,
            "expiry_timestamp": None,
            "departed_countdown_active": True,
            "departed_countdown_expiry": int(cooldown_expiry.timestamp()) if cooldown_expiry else None,
        })
        entries.append(entry)

    return entries


def get_queue_state(route_filter=None, persist_boarding_start=False):
    now = timezone.now()
    # ensure expirations captured before computing payload
    run_queue_housekeeping(now=now)
    settings = SystemSettings.get_solo()
    departure_duration = getattr(settings, "departure_duration_minutes", 30)
    departed_cutoff = now - timedelta(seconds=DEPARTED_VISIBLE_SECONDS)

    logs = (
        EntryLog.objects
        .select_related("vehicle", "vehicle__assigned_driver", "vehicle__route")
        .filter(status=EntryLog.STATUS_SUCCESS)
        .filter(Q(is_active=True) | Q(departed_at__gte=departed_cutoff))
        .order_by("vehicle__route__origin", "vehicle__route__destination", "created_at")
    )

    if route_filter:
        logs = logs.filter(vehicle__route_id=route_filter)

    route_groups = OrderedDict()
    for log in logs:
        route = getattr(log.vehicle, "route", None)
        route_key = route.id if route else None
        route_name = f"{route.origin} → {route.destination}" if route else "Unassigned"
        route_groups.setdefault(route_key, {
            "route_name": route_name,
            "route_id": route_key,
            "logs": [],
        })
        route_groups[route_key]["logs"].append(log)

    entries = []
    for group in route_groups.values():
        entries.extend(_build_route_entries(
            group["route_name"],
            group["route_id"],
            group["logs"],
            now,
            departure_duration,
            departed_cutoff,
            DEPARTED_COUNTDOWN_SECONDS,
            persist_boarding_start,
        ))

    counts = {
        "queued": sum(1 for entry in entries if entry["status"] == "Queued"),
        "boarding": sum(1 for entry in entries if entry["status"] == "Boarding"),
    }

    history = _collect_history(route_filter=route_filter)

    return {
        "entries": entries,
        "counts": counts,
        "departure_duration_minutes": departure_duration,
        "history": history,
        "server_time": int(now.timestamp()),
    }


def _collect_history(route_filter=None):
    queryset = (
        QueueHistory.objects
        .select_related("vehicle__route")
        .order_by("-timestamp")
    )

    if route_filter:
        queryset = queryset.filter(vehicle__route_id=route_filter)

    history_by_route = OrderedDict()
    for event in queryset:
        route = getattr(event.vehicle, "route", None)
        route_name = str(route) if route else "Unassigned Route"
        entries = history_by_route.setdefault(route_name, [])
        if len(entries) >= HISTORY_LIMIT_PER_ROUTE:
            continue

        vehicle_plate = getattr(event.vehicle, "license_plate", "—") if event.vehicle else "—"
        entries.append({
            "vehicle_plate": vehicle_plate,
            "action": event.get_action_display(),
            "timestamp": timezone.localtime(event.timestamp).strftime("%I:%M %p"),
        })

    return history_by_route
