from django.contrib.sessions import serializers
from rest_framework.serializers import ModelSerializer

from API.models import Glos


class GlosSerializer(ModelSerializer):
    class Meta:
        model = Glos
        fields = ('uzytkownik', 'wynik','czas_oddania')

