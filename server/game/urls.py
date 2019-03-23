from django.urls import path
from django.conf.urls import url

from .views import *

urlpatterns = [
    path("join", join),
    path("login", login_session),
    path("payQrCode",qr_code_payment),
    path("payPhone", phone_number_payment),
    path("register", register),
    path("load", load)
]
