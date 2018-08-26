import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from API.models import Glos
from API.serializers import GlosSerializer

@receiver(post_save, sender=Glos)
def announce_new_user(sender, **kwargs):
    instance = kwargs['instance']


    object_list = json.dumps(GlosSerializer(instance).data)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'wyniki',
        #user.glos to wywoalanie metody user_glos
        {"type": "user.glos",
         "event": "Nowy glos",
         "object_list": object_list})