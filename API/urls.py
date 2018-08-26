from django.urls import path
from API import views
from django.contrib.auth import views as auth


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', auth.LogoutView.as_view(next_page='/')),
    path('fusion/', views.myFirstChart, name='fusion'),
    path('chat/', views.chat, name='chat'),
]
