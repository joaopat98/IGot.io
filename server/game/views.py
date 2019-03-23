from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import Score
from .forms import UserCreationForm, ProfileForm
from .data import *

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
    request.session["name"] = request.POST["name"]
    score = Score.objects.filter(name=request.POST["name"]).first()
    if score is None:
        Score.objects.create(name=request.POST["name"])
    player = new_player(request.POST["name"])
    request.session["player"] = player.uid
    return HttpResponse()


def load(request):
    player = players[request.session["player"]]
    return JsonResponse({
        "playerX": player.x,
        "playerY": player.y,
        "id": player.uid,
        "mapWidth": map_width,
        "mapHeight": map_height,
        "charSize": char_size,
        "speed": speed
    }, safe=False)
