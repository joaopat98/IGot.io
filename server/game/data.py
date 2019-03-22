import datetime
import json
from threading import Thread, Lock
from random import Random
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from opensimplex import OpenSimplex

players = {}
bots = {}
NUM_BOTS = 100
max_id = 0
TIME_DIV = 1000
epoch = datetime.datetime.utcfromtimestamp(0)
map_width = 3000
map_height = 3000
char_size = 80
old_t = (datetime.datetime.now() - epoch).total_seconds()
speed = 500


def synchronized(func):
    func.__lock__ = Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


@synchronized
def new_player():
    global max_id
    c = Character(1000, 1000, rand, max_id, 1)
    players[c.uid] = c
    max_id += 1
    return c


class Character:
    def __init__(self, max_x, max_y, random, uid, speed):
        self.x = (random.random() - 0.5) * max_x
        self.y = (random.random() - 0.5) * max_y
        self.uid = uid
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
        self.x += valx * self.speed * (t - old_t)
        self.y += valy * self.speed * (t - old_t)

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


rand = Random()
for i in range(NUM_BOTS):
    bots[max_id] = Character(map_width, map_height, rand, max_id, speed)
    max_id += 1

updater = Updater()
updater.start()
