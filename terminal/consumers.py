from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .constants import QUEUE_GROUP_NAME, TV_DISPLAY_GROUP_NAME


class QueueConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for public queue display.
    Sends full queue state including queued, boarding, and departed vehicles.
    """

    async def connect(self):
        await self.channel_layer.group_add(QUEUE_GROUP_NAME, self.channel_name)
        await self.accept()
        await self.send_queue_state()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(QUEUE_GROUP_NAME, self.channel_name)

    async def queue_update(self, event):
        """Handle queue update broadcast."""
        payload = event.get("payload")
        if payload:
            await self.send_json(payload)

    async def send_queue_state(self):
        """Send initial queue state on connection."""
        from .services import QueueService
        queue_state = await sync_to_async(QueueService.get_queue_state)()
        await self.send_json(queue_state)


class TVDisplayConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for terminal TV display.
    Shows boarding and departed only, with queued count as badge.
    Preserves fullscreen mode by using partial DOM updates.
    """

    async def connect(self):
        # Join both groups to receive all updates
        await self.channel_layer.group_add(TV_DISPLAY_GROUP_NAME, self.channel_name)
        await self.channel_layer.group_add(QUEUE_GROUP_NAME, self.channel_name)
        await self.accept()
        await self.send_tv_state()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(TV_DISPLAY_GROUP_NAME, self.channel_name)
        await self.channel_layer.group_discard(QUEUE_GROUP_NAME, self.channel_name)

    async def tv_update(self, event):
        """Handle TV display update broadcast."""
        payload = event.get("payload")
        if payload:
            await self.send_json(payload)

    async def queue_update(self, event):
        """Also listen to general queue updates."""
        # Reformat for TV display
        await self.send_tv_state()

    async def send_tv_state(self):
        """Send TV display state on connection or update."""
        from .services import QueueService
        tv_state = await sync_to_async(QueueService.get_tv_display_state)()
        await self.send_json(tv_state)
