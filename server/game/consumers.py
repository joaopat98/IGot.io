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
        if obj["action"] == "move":
            players[self.scope["session"]["player"]].x += obj["deltaX"]
            players[self.scope["session"]["player"]].y += obj["deltaY"]

        # Receive message from room group

    def message(self, event):
        message = event['message']
        self.send(message)

