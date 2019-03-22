import datetime
import json
from threading import Thread
from random import Random
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from opensimplex import OpenSimplex

players = []
bots = []
NUM_BOTS = 100
max_id = 0
TIME_DIV = 1000
epoch = datetime.datetime.utcfromtimestamp(0)


class Bot:
    def __init__(self, max_x, max_y, random, uid, speed):
        self.x = random.random() * max_x
        self.y = random.random() * max_y
        self.uid = uid
        self.offsetX = random.random()
        self.offsetY = random.random()
        self.noiseX = OpenSimplex(seed=random.randint(0, 1000000000))
        self.noiseY = OpenSimplex(seed=random.randint(0, 1000000000))
        self.speed = speed
        self.skin = rand.randint(0, 10)

    def update(self, t):
        self.x += self.noiseX.noise2d(1, t + self.offsetX) * self.speed
        self.y += self.noiseY.noise2d(1, t + self.offsetY) * self.speed

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
            secs = (datetime.datetime.now() - epoch).total_seconds()

            for bot in bots:
                bot.update(secs)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)("test", {
                "type": "message",
                "message": json.dumps(list(map(lambda b: b.serialize(), bots)))
            })


rand = Random()
for i in range(NUM_BOTS):
    bots.append(Bot(1000, 1000, rand, max_id, 1))
    max_id += 1

updater = Updater()
updater.start()
