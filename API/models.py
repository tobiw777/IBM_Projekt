from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Code(models.Model):
    token = models.CharField(max_length=6, null=False, default='789456')
    def __str__(self):
        return str(self.token)


class Survey(models.Model):
    PLEC = (
        ('M', 'Mężczyzna'),
        ('K', 'Kobieta'),
    )
    WYKSZTALCENIE = (
        ('p', 'Podstawowe'),
        ('g', 'Gimnazjalne'),
        ('s', 'Średnie'),
        ('w', 'Wyższe'),
    )
    TN = (
        (True, 'TAK'),
        (False, 'NIE'),
    )
    uzytkownik= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    wiek = models.SmallIntegerField(null=False, default=20)
    plec = models.CharField(max_length=1, choices=PLEC, null=False, default='M')
    wyksztalcenie = models.CharField(max_length=1, choices=WYKSZTALCENIE, null=False, default='p')
    zaAI = models.BooleanField(choices=TN, null=False, default=True)

    def __str__(self):
        return str(self.uzytkownik.username)


class Glos(models.Model):

    TN = (
        (True, 'TAK'),
        (False, 'NIE'),
    )

    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    wynik = models.BooleanField(choices=TN, blank=False, default=True)
    czas_oddania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        dict = {True: 'TAK', False: 'NIE'}
        return str(self.uzytkownik.username + ' - '  + ' Oddany glos: '+ str(dict.get(self.wynik)))


