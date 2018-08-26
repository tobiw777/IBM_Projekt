from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import Code
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
                return redirect('/')
            else:
                print("Zle zczytuje dane")
        else:
            print('UPS cos poszlo nie tak!')

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

from collections import OrderedDict

# Include the `fusioncharts.py` file that contains functions to embed the charts.


def myFirstChart(request):

    #Chart data is passed to the `dataSource` parameter, as dictionary in the form of key - value pairs.
    dataSource = OrderedDict()

    # The `chartConfig` dict contains key - value pairs data for chart attribute
    chartConfig = OrderedDict()
    chartConfig["caption"] = "Countries With Most Oil Reserves [2017-18]"
    chartConfig["subCaption"] = "In MMbbl = One Million barrels"
    chartConfig["xAxisName"] = "Country"
    chartConfig["yAxisName"] = "Reserves (MMbbl)"
    chartConfig["numberSuffix"] = "K"
    chartConfig["theme"] = "fusion"

    # The `chartData` dict contains key - value pairs data
    chartData = OrderedDict()
    chartData["Venezuela"] = 290
    chartData["Saudi"] = 260
    chartData["Canada"] = 180
    chartData["Iran"] = 140
    chartData["Russia"] = 115
    chartData["UAE"] = 100
    chartData["US"] = 30
    chartData["China"] = 30

    dataSource["chart"] = chartConfig
    dataSource["data"] = []

    # Convert the data in the `chartData`array into a format that can be consumed by FusionCharts.
    #The data for the chart should be in an array wherein each element of the array
    #is a JSON object# having the `label` and `value` as keys.

    #Iterate through the data in `chartData` and insert in to the `dataSource['data']` list.
    for key, value in chartData.items():
        data = {}
        data["label"] = key
        data["value"] = value
        dataSource["data"].append(data)
    print(dataSource['data'])


# Create an object for the column 2D chart using the FusionCharts class constructor
# The chart data is passed to the `dataSource` parameter.
    column2D = FusionCharts("column2d", "myFirstChart", "600", "400", "myFirstchart-container", "json", dataSource)

    return render(request, 'fusion.html', {
        'output': column2D.render()
    })


def chat(request):
    user = request.user
    return render(request, 'chat.html', {
        'user': user
    })
