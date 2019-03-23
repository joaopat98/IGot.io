from django.urls import path
from django.conf.urls import url

from .views import *

urlpatterns = [
    path("join", join),
    path("login", login_session),
    path("register", register),
]
