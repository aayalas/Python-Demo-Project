from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='dash'),
    path('', views.settings, name='settings'),
]

