from django.urls import path

from . import views

import mec.dash_apps

urlpatterns = [
    path('', views.MecIndex.as_view(), name='index'),
]