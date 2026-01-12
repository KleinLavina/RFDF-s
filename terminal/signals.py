from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .constants import QUEUE_GROUP_NAME
from .models import EntryLog, TerminalActivity
from .utils import format_route_display
from vehicles.models import QueueHistory
from .queue_state import get_queue_state


def publish_queue_update():
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    payload = get_queue_state()
    async_to_sync(channel_layer.group_send)(
        QUEUE_GROUP_NAME,
        {
            "type": "queue.update",
            "payload": payload,
        },
    )


@receiver(post_save, sender=EntryLog)
def handle_entrylog_save(sender, instance, **kwargs):
    publish_queue_update()


@receiver(post_delete, sender=EntryLog)
def handle_entrylog_delete(sender, instance, **kwargs):
    publish_queue_update()


@receiver(post_save, sender=QueueHistory)
def sync_terminal_activity_from_queue(sender, instance, created, **kwargs):
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
