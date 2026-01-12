from django.utils import timezone

from terminal.shared_queue import (
    apply_entry_log_maintenance,
    PASSENGER_DELETE_AFTER_MINUTES,
)


def maintenance_task(now=None):
    """
    Shared helper to keep the public queue maintenance logic centralized.
    Returns the (current time, departure_duration, departed_cutoff) tuple.
    """
    now = now or timezone.now()
    return apply_entry_log_maintenance(
        now=now,
        delete_after_minutes=PASSENGER_DELETE_AFTER_MINUTES,
    )
