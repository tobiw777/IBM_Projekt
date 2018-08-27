import json
import asyncio
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from . import models
from .serializers import GlosSerializer


class GlosowanieConsumer(AsyncJsonWebsocketConsumer):

    #metoda do laczenia z websocketem
    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add(
            'chat',
            self.channel_name
        )

        await self.channel_layer.group_add(
            'wyniki',
            self.channel_name
        )


        votes = models.Glos.objects.all()
        za = votes.filter(wynik=True).count()
        przeciw = votes.filter(wynik=False).count()

        #vote_serialized = GlosSerializer(votes, many=True).data

        # Zliczone glosy za i przeciw a takze json z wynikami w "ladnej postaci"

        wyn = []
        for vote in votes:
            wyn.append({'Uzytkownik': vote.uzytkownik.username, 'wynik': vote.wynik, "czas": vote.czas_oddania.strftime('%H:%M:%S')})
        print(json.dumps(wyn))

        # pobranie wszystkich glosow dla danego glosowania i wyslanie jej do websocketu po dolaczeniu do grupy
        await self.channel_layer.group_send(
            'wyniki',
            {"type": "user.glos",
             "event": "Lista glosow",
             "message": "Wczytane glosy",
             "votes": wyn,
             "za": za,
             "przeciw": przeciw
             }
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        username = 'default'
        user = self.scope['user']
        if user.is_authenticated:
            username = user.username

        data = json.loads(text_data)
        print(data)
        d = data.get('Message')

        await self.channel_layer.group_send(
            'chat',
            {"type": "user.glos",
             "event": "Wiadomosc",
             "message": d,
             "username": username
             }
        )
    #metoda do odlaczenia od websocketu
    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            'chat',
            self.channel_name
        )

    #metoda do wysylania glosu do websocketu
    async def user_glos(self, event):
        await self.send_json(event)


# Nie korzystam narazie z tego:

class WynikiConsumer(AsyncJsonWebsocketConsumer):

    #metoda do laczenia z websocketem
    async def connect(self):
        await self.accept()

        await self.channel_layer.group_add(
            'chat',
            self.channel_name
        )

        votes = models.Glos.objects.all()
        za = votes.filter(wynik=True).count()
        przeciw = votes.filter(wynik=False).count()

        vote_serialized = GlosSerializer(votes, many=True).data

        wyn = []
        for vote in votes:
            wyn.append({'Uzytkownik': vote.uzytkownik.username, 'wynik': vote.wynik, "czas": vote.czas_oddania.strftime('%H:%M:%S')})
        print(json.dumps(wyn))

        # pobranie wszystkich glosow dla danego glosowania i wyslanie jej do websocketu po dolaczeniu do grupy
        await self.channel_layer.group_send(
            'chat',
            {"type": "user.glos",
             "event": "Nowy glos",
             "message": "Wczytane glosy",
             "votes": wyn,
             "za": za,
             "przeciw": przeciw
             }
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        username = 'default'
        user = self.scope['user']
        if user.is_authenticated:
            username = user.username

        data = json.loads(text_data)
        print(data)
        d = data.get('Message')
        
        await self.channel_layer.group_send(
            'chat',
            {"type": "user.glos",
             "event": "Nowy glos",
             "message": d,
             "username": username
             }
        )
    #metoda do odlaczenia od websocketu
    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            'chat',
            self.channel_name
        )

    #metoda do wysylania glosu do websocketu
    async def user_glos(self, event):
        await self.send_json(event)

