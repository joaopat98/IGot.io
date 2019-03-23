# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
import json

from .models import Score
from .data import *


def updateScore(score, name):
    s = Score.objects.filter(name=name).first()
    s.score = max(s.score, score)
    s.save()


class GameConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            "test",
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            "test",
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        obj = json.loads(text_data)
        player = players[self.scope["session"]["player"]]
        if obj["action"] == "move":
            new_x = player.x + obj["deltaX"]
            new_y = player.y + obj["deltaY"]
            player.x = max(min(new_x, map_width / 2 - char_size / 2), -map_width / 2 + char_size / 2)
            player.y = max(min(new_y, map_height / 2 - char_size / 2), -map_height / 2 + char_size / 2)

        elif obj["action"] == "fire":
            target = get_target(player, obj["rotation"])
            if target is not None:
                if target.is_player:
                    player.score += player_kill
                    database_sync_to_async(updateScore(player.score, self.scope["session"]["name"]))
                    target.reset()
                else:
                    player.score -= bot_kill
                    database_sync_to_async(updateScore(player.score, self.scope["session"]["name"]))
                    del bots[target.uid]

        # Receive message from room group

    def message(self, event):
        message = event['message']
        self.send(message)
