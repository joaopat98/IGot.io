from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import Score, UserSkins
from .forms import UserCreationForm, ProfileForm
from .data import *
from . import mbway_api

# Create your views here.
from .data import new_player


def error_dict(*args):
    final = dict()
    for item in args:
        if item is not None:
            if issubclass(type(item), ModelForm):
                errors = dict()
                for error in item.errors.keys():
                    errors[error] = item.errors[error][0]
                final = {**final, **errors}
            else:
                final = {**final, **item}
    return final


def register(request):
    if request.method == "POST":
        errors = {}
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            UserSkins.objects.create(profile=profile, skin=Skin.objects.filter(slang="default").first())
            return JsonResponse(user.id, safe=False)
        else:
            return JsonResponse(error_dict(user_form, profile_form, errors), status=400)
    else:
        return HttpResponseNotAllowed("Method not Allowed")


def login_session(request):
    if request.method == "POST":
        try:
            user = authenticate(
                username=request.POST["username"], password=request.POST["password"])
        except KeyError as k:
            return JsonResponse({k.args[0]: "field missing in form"}, status=400)
        if user is not None:
            login(request, user)
            return HttpResponse()
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotAllowed("Method not Allowed")


def join(request):
    if request.user.is_authenticated:
        request.session["name"] = request.user.username
    else:
        request.session["name"] = request.POST["name"]
    score = Score.objects.filter(name=request.session["name"]).first()
    if score is None:
        Score.objects.create(name=request.session["name"])
    player = new_player(request.session["name"], request.user)
    request.session["player"] = player.uid
    return HttpResponse()


def load(request):
    player = players[request.session["player"]]
    skins = {}
    for skin in Skin.objects.all():
        skins[skin.slang] = skin.path_png
    return JsonResponse({
        "playerX": player.x,
        "playerY": player.y,
        "id": player.uid,
        "mapWidth": map_width,
        "mapHeight": map_height,
        "charSize": char_size,
        "fov": fov,
        "speed": speed,
        "playerSkin": player.skin,
        "skins": skins

    }, safe=False)


def phone_number_payment(request):
    if request.method == "POST":
        identifier = request.POST["identifier"]
        number = request.POST["number"]
        value = request.POST["value"]
        data = {"identifier": identifier, "number": number, "value": value}
        code = mbway_api.phone_number_option(data)
        if code == 200:
            UserSkins.objects.create(profile=request.user.user_profile,
                                     skin=Skin.objects.filter(slang=request.POST["skin"]).first())
        return HttpResponse(status=code)
    else:
        return HttpResponseNotAllowed("Method not Allowed")


def qr_code_payment(request):
    if request.method == "POST":
        data = mbway_api.generate(request.POST["value"])
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseNotAllowed("Method not Allowed")


def qr_inquiry(request):
    if request.method == "POST":
        code = request.POST["qrCodeToken"]
        if code == 200:
            UserSkins.objects.create(profile=request.user.user_profile,
                                     skin=Skin.objects.filter(slang=request.POST["skin"]).first())
        return HttpResponse(mbway_api.inquiryQR(code))
    else:
        return HttpResponseNotAllowed("Method not Allowed")
