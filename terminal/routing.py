from django.urls import re_path

from .consumers import QueueConsumer, TVDisplayConsumer

websocket_urlpatterns = [
    re_path(r"ws/queue/$", QueueConsumer.as_asgi()),
    re_path(r"ws/tv-display/$", TVDisplayConsumer.as_asgi()),
]
