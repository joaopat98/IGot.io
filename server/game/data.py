import atexit
import datetime
import json
from math import sqrt, floor, cos
from threading import Thread, Lock, Event
from random import Random
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from opensimplex import OpenSimplex
from math import atan2, degrees, radians, tan, sin
from .models import Skin
import sys


print(sys.argv)

players = {}
bots = {}
NUM_BOTS = 50
max_id = 0
TIME_DIV = 1000
epoch = datetime.datetime.utcfromtimestamp(0)
map_width = 3000
map_height = 3000
char_size = 80
old_t = (datetime.datetime.now() - epoch).total_seconds()
speed = 250
fov = 450
baseY = 0
bot_kill = 1
player_kill = 5


def mod(a, n):
    return a - floor(a / n) * n


def is_in_range(x, y, ang):
    y = -y
    p_1 = cos(radians(ang)) * fov
    p_2 = sin(radians(ang)) * fov
    if p_1 * x + p_2 * y < 0:
        return False
    magn = sqrt(p_1 ** 2 + p_2 ** 2)
    p_1 /= magn
    p_2 /= magn
    v = abs(p_1 * y - p_2 * x)
    return v <= char_size / 2


def dist(player, target):
    return sqrt((player.x - target.x) ** 2 + (player.y - target.y) ** 2)


def get_target(player, angle):
    angle = -angle
    possible_bots = list(filter(lambda b: player.x - fov < b.x < player.x + fov and
                                          player.y - fov < b.y < player.y + fov, bots.values()))
    possible_players = list(filter(lambda p: player.x - fov < p.x < player.x + fov and
                                             player.y - fov < p.y < player.y + fov, players.values()))
    possible_chars = possible_bots + possible_players
    possible_chars = list(filter(lambda c: dist(player, c) <= fov, possible_chars))
    possible_chars.sort(key=lambda char: dist(player, char))

    while angle < 0:
        angle += 360
    angle = angle % 360
    final = None
    for char in possible_chars:
        if char.uid != player.uid:
            if is_in_range(char.x - player.x, char.y - player.y, angle):
                final = char
                break
    return final


def synchronized(func):
    func.__lock__ = Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


@synchronized
def new_player(name, user):
    global max_id
    if user.is_authenticated:
        c = Character(1000, 1000, rand, max_id, 1, True, name, user.user_profile.current_skin)
    else:
        c = Character(1000, 1000, rand, max_id, 1, True, name)
    players[c.uid] = c
    max_id += 1
    return c


class Character:
    def __init__(self, max_x, max_y, random, uid, speed, is_player, name=None, skin_slang="default"):
        self.x = (random.random() - 0.5) * max_x
        self.y = (random.random() - 0.5) * max_y
        self.name = name
        self.score = 10
        self.max_x = max_x
        self.max_y = max_y
        self.random = random
        self.uid = uid
        self.is_player = is_player
        self.offsetX = random.random()
        self.offsetY = random.random()
        self.noiseX = OpenSimplex(seed=random.randint(0, 1000000000))
        self.noiseY = OpenSimplex(seed=random.randint(0, 1000000000))
        self.speed = speed
        if sys.argv[1] == "runserver":
            if not is_player:
                self.skin = list(Skin.objects.all())[rand.randint(0, Skin.objects.count() - 1)].slang
            else:
                self.skin = Skin.objects.filter(slang=skin_slang).first().slang

    def reset(self):
        self.x = (self.random.random() - 0.5) * self.max_x
        self.y = (self.random.random() - 0.5) * self.max_y
        self.score = 10

    def update(self, t):
        valx = self.noiseX.noise2d(1, t + self.offsetX)
        valy = self.noiseY.noise2d(1, t + self.offsetY)
        if valx > 0.3:
            valx = 1
        elif valx < -0.3:
            valx = -1
        else:
            valx = 0
        if valy > 0.3:
            valy = 1
        elif valy < -0.3:
            valy = -1
        else:
            valy = 0
        m = valx * valx + valy * valy
        if m != 0:
            valx /= m
            valy /= m
        new_x = self.x + valx * self.speed * (t - old_t)
        new_y = self.y + valy * self.speed * (t - old_t)
        self.x = max(min(new_x, map_width / 2 - char_size / 2), -map_width / 2 + char_size / 2)
        self.y = max(min(new_y, map_height / 2 - char_size / 2), -map_height / 2 + char_size / 2)

    def serialize(self):
        return {
            "x": self.x,
            "y": self.y,
            "id": self.uid,
            "skin": self.skin,
            "score": self.score
        }


class Updater(Thread):
    def __init__(self):
        super(Updater, self).__init__()
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self._stop_event.is_set():
            global old_t

            secs = (datetime.datetime.now() - epoch).total_seconds()

            for bot in bots.values():
                bot.update(secs)
            old_t = secs
            channel_layer = get_channel_layer()
            player_list = list(players.values())
            player_list.sort(key=lambda p: p.score, reverse=True)
            selected = list(map(lambda p: {"name": p.name, "score": p.score}, player_list[:min(10, len(player_list))]))
            async_to_sync(channel_layer.group_send)("test", {
                "type": "message",
                "message": json.dumps({
                    "chars": list(map(lambda b: b.serialize(), bots.values())) +
                             list(map(lambda p: p.serialize(), players.values())),
                    "leaderboard": selected,
                    "number_players": len(players.keys())
                })
            })


rand = Random()
for i in range(NUM_BOTS):
    bots[max_id] = Character(map_width, map_height, rand, max_id, speed, False)
    max_id += 1

updater = Updater()
if sys.argv[1] == "runserver":
    updater.start()
