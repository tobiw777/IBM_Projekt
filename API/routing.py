from django.urls import path
from .consumers import WynikiConsumer, GlosowanieConsumer

websocket_url = [
    path('chat/', GlosowanieConsumer),
    path('', GlosowanieConsumer)
]