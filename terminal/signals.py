from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .constants import QUEUE_GROUP_NAME, TV_DISPLAY_GROUP_NAME
from .models import EntryLog, TerminalActivity, Transaction
from .utils import format_route_display
from vehicles.models import QueueHistory


def publish_queue_update():
    """Broadcast queue update to all WebSocket clients."""
    from .services import QueueService
    QueueService.broadcast_queue_update()


def publish_tv_update():
    """Broadcast TV display update to all WebSocket clients."""
    from .services import QueueService
    
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    payload = QueueService.get_tv_display_state()
    async_to_sync(channel_layer.group_send)(
        TV_DISPLAY_GROUP_NAME,
        {
            "type": "tv.update",
            "payload": payload,
        },
    )


@receiver(post_save, sender=EntryLog)
def handle_entrylog_save(sender, instance, created, **kwargs):
    """Handle entry log save - broadcast updates."""
    publish_queue_update()
    publish_tv_update()

    # Create transaction record when entry log is marked as departed
    if not created and not instance.is_active and instance.departed_at:
        # Check if transaction already exists
        existing = Transaction.objects.filter(entry_log=instance).exists()
        if not existing and instance.status == EntryLog.STATUS_SUCCESS:
            Transaction.create_from_entry_log(instance)


@receiver(post_delete, sender=EntryLog)
def handle_entrylog_delete(sender, instance, **kwargs):
    """Handle entry log deletion - broadcast updates."""
    publish_queue_update()
    publish_tv_update()


@receiver(post_save, sender=QueueHistory)
def sync_terminal_activity_from_queue(sender, instance, created, **kwargs):
    """Sync queue history to terminal activity for reporting."""
    if not created:
        return

    route = format_route_display(getattr(instance.vehicle, "route", None))
    TerminalActivity.objects.update_or_create(
        queue_history=instance,
        defaults={
            "vehicle": instance.vehicle,
            "driver": instance.driver,
            "route_name": route,
            "event_type": instance.action,
            "fee_charged": instance.fee_charged,
            "wallet_balance_snapshot": instance.wallet_balance_snapshot,
            "timestamp": instance.timestamp,
        },
    )

    # Broadcast updates after activity sync
    publish_queue_update()
    publish_tv_update()
