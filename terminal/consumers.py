from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .constants import QUEUE_GROUP_NAME
from .queue_state import get_queue_state


class QueueConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(QUEUE_GROUP_NAME, self.channel_name)
        await self.accept()
        await self.send_queue_state()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(QUEUE_GROUP_NAME, self.channel_name)

    async def queue_update(self, event):
        payload = event.get("payload")
        if payload:
            await self.send_json(payload)

    async def send_queue_state(self):
        queue_state = await sync_to_async(get_queue_state)()
        await self.send_json(queue_state)
