import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.chat_message({
            "type": "chat_message",
            "message": self.generateMessage("Welcome!", "Admin")
        })
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "except": self.channel_name,
                "message": self.generateMessage(f"{self.user} has joined!", "Admin")
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data["message"]
        print(f"Message: {message}")

    def generateMessage(self, text, username):
        return {
            "username": username,
            "text": text,
            "createdAt": datetime.datetime.now()
        }

    async def chat_message(self, event):
        msg = event["message"]
        if ("except" in event and event["except"] == self.channel_name):
            return
            
        await self.send(text_data=json.dumps({
            "type": "message",
            "data": msg
        }, sort_keys=True, indent=1, cls=DjangoJSONEncoder))