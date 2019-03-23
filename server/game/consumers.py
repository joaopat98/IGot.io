# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .data import *


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
            player.x += obj["deltaX"]
            player.y += obj["deltaY"]
        elif obj["action"] == "fire":
            target = get_target(player, obj["rotation"])
            if target is not None:
                if target.is_player:
                    del players[target.uid]
                else:
                    del bots[target.uid]


        # Receive message from room group

    def message(self, event):
        message = event['message']
        self.send(message)

