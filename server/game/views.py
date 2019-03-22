from django.http import JsonResponse
from django.shortcuts import render
from .data import *

# Create your views here.
from .data import new_player


def join(request):
    player = new_player()
    request.session["player"] = player.uid
    return JsonResponse({
        "playerX": player.x,
        "playerY": player.y,
        "id": player.uid,
        "mapWidth": map_width,
        "mapHeight": map_height,
        "charSize": char_size,
        "speed": speed
    }, safe=False)
