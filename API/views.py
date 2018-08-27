from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, GlosForm
from .models import Code, Glos
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .static.fusioncharts import FusionCharts
from django.http import HttpResponse

# Create your views here.


def index(request):
    user = request.user
    return render(request, 'index.html', {'user': user})


def register(request):
    kod = Code.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.errors)

        if form.is_valid():
            odp = form.cleaned_data.get('token')
            print(odp)
            if kod.filter(token=odp):
                username = 'User{}'.format(User.objects.count() + 1)
                User.objects.create_user(username, '', '')
                user = authenticate(username=username, password='')
                login(request, user)
                print("Wszystko poszlo ok!")
                return redirect('API:index')
            else:
                print("Zle zczytuje dane")
        else:
            print('UPS cos poszlo nie tak!')

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
# do wywalenia

from collections import OrderedDict

# Include the `fusioncharts.py` file that contains functions to embed the charts.

@login_required
def vote(request):

    if request.method == 'POST':
        form=GlosForm(request.POST)
        print(form.errors)
        if form.is_valid():
            wynik = form.cleaned_data.get('wynik')
            user=None

            if request.user.is_authenticated:
                user = request.user
                print('user '+ user.username)

            Glos.objects.create(uzytkownik=user,wynik=wynik)

            #return HttpResponseNotModified()
            return redirect('API:index')
        else:
            print('UPS cos poszlo nie tak!')

    else:
        form =GlosForm()
        return render(request, 'vote.html', {'form': form})