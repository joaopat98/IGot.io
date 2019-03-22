import datetime
import json
from math import sqrt
from threading import Thread, Lock
from random import Random
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from opensimplex import OpenSimplex
from math import atan2, degrees, radians, tan, sin

players = {}
bots = {}
NUM_BOTS = 10
max_id = 0
TIME_DIV = 1000
epoch = datetime.datetime.utcfromtimestamp(0)
map_width = 3000
map_height = 3000
char_size = 80
old_t = (datetime.datetime.now() - epoch).total_seconds()
speed = 250
fov = 600
baseY = 0


def is_in_range(x, y, ang):
    global baseY
    m = tan(radians(ang))
    baseY = abs(m * x)
    if (-y > 0 and ang == 90) or (-y < 0 and ang == 270):
        return -char_size / 2 <= x <= char_size / 2
    if (x > 0 and ang == 0) or (x < 0 and ang == 180):
        return -char_size / 2 <= -y <= char_size / 2
    delta = abs(char_size / 2 / sin(radians(ang)))
    if x > 0:
        if ang < 90:
            return -baseY - delta <= y <= -baseY + delta
        elif ang > 270:
            return baseY - delta <= y <= baseY + delta
        return False
    elif x < 0:
        if ang < 180:
            return -baseY - delta <= y <= -baseY + delta
        elif ang > 180:
            return baseY - delta <= y <= baseY + delta
        return False


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
def new_player():
    global max_id
    c = Character(1000, 1000, rand, max_id, 1, True)
    players[c.uid] = c
    max_id += 1
    return c


class Character:
    def __init__(self, max_x, max_y, random, uid, speed, is_player):
        self.x = (random.random() - 0.5) * max_x
        self.y = (random.random() - 0.5) * max_y
        self.uid = uid
        self.is_player = is_player
        self.offsetX = random.random()
        self.offsetY = random.random()
        self.noiseX = OpenSimplex(seed=random.randint(0, 1000000000))
        self.noiseY = OpenSimplex(seed=random.randint(0, 1000000000))
        self.speed = speed
        self.skin = rand.randint(0, 10)

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
            "skin": self.skin
        }


class Updater(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.shouldRun = True

    def run(self):
        while self.shouldRun:
            global old_t

            secs = (datetime.datetime.now() - epoch).total_seconds()

            for bot in bots.values():
                bot.update(secs)
            old_t = secs
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)("test", {
                "type": "message",
                "message": json.dumps({
                    "chars": list(map(lambda b: b.serialize(), bots.values())) +
                             list(map(lambda p: p.serialize(), players.values()))
                })
            })
            sleep(1/100)


rand = Random()
for i in range(NUM_BOTS):
    bots[max_id] = Character(map_width, map_height, rand, max_id, speed, False)
    max_id += 1

updater = Updater()
updater.start()
