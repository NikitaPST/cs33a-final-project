import datetime
import http.client
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder

from .room_manager import RoomManager

class ChatConsumer(AsyncWebsocketConsumer):
    room_manager = RoomManager()

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name.replace(' ', '_')}"
        self.user = self.scope["user"]
        ChatConsumer.room_manager.add_user(
            self.channel_name,
            self.user,
            self.room_name
        )
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.chat_message({
            "type": "chat_message",
            "message": self.generate_message("Welcome! (type !help for additional commands)", "Admin")
        })
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "except": self.channel_name,
                "message": self.generate_message(
                    f"{self.user} has joined!", "Admin"
                )
            }
        )
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "room_data",
                "room": self.room_name,
                "users": ChatConsumer.room_manager.get_users_in_room(
                    self.room_name
                )
            }
        )

    async def disconnect(self, close_code):
        ChatConsumer.room_manager.remove_user(self.channel_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": self.generate_message(
                    f"{self.user} has left!", "Admin"
                )
            }
        )
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "room_data",
                "room": self.room_name,
                "users": ChatConsumer.room_manager.get_users_in_room(
                    self.room_name
                )
            }
        )

    async def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data["message"]
        params = message.split()
        if params[0] == "!help":
            message = "Additional commands:\n" \
                + "!location - returns your location\n" \
                + "!weather - returns current weather\n" \
                + "!image [url] - post image to chat"
            await self.chat_message({
                    "type": "chat_message",
                    "message": self.generate_message(
                        message, "Admin"
                    )
                }
            )
        elif params[0] == "!location":
            latitude = params[1]
            longitude = params[2]
            location = self.get_location(latitude, longitude)
            message = f"Your current location: {location}" \
                if location is not None \
                else "Can't determine your location"
            await self.chat_message({
                    "type": "chat_message",
                    "message": self.generate_message(
                        message, "Admin"
                    )
                }
            )
        elif params[0] == "!weather":
            latitude = params[1]
            longitude = params[2]
            forecast = self.get_forecast(latitude, longitude)
            message = f"Current weather at {forecast['place']}:\n" \
                + f"Temperature: {forecast['temp']} \u2109\n" \
                + forecast["description"].title() + "\n" \
                + f"Wind speed: {forecast['wind_speed']} miles/hour" \
                if forecast is not None \
                else "Can't determine weather in your region"
            await self.chat_message({
                "type": "chat_message",
                "message": self.generate_message(
                    message, "Admin"
                )
            })
        elif params[0] == "!image":
            url = params[1]
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_image",
                    "message": self.generate_image(
                        url, str(self.user)
                    )
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": self.generate_message(
                        message, str(self.user)
                    )
                }
            )
        

    def generate_message(self, text, username):
        return {
            "username": username,
            "text": text,
            "createdAt": datetime.datetime.now()
        }

    def generate_image(self, image, username):
        return {
            "username": username,
            "image": image,
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

    async def chat_image(self, event):
        msg = event["message"]

        await self.send(text_data=json.dumps({
            "type": "image",
            "data": msg
        }, sort_keys=True, indent=1, cls=DjangoJSONEncoder))

    async def room_data(self, event):
        data = {
            "room": event["room"],
            "users": event["users"]
        }
        await self.send(text_data=json.dumps({
            "type": "roomData",
            "data": data
        }))

    def get_location(self, latitude, longitude):
        location = None
        host = "us1.locationiq.com"
        api_key = "pk.2cbf57d26ecd52c509e8895aefd8e4f8"
        url = f"/v1/reverse.php?key={api_key}" \
            + f"&lat={latitude}&lon={longitude}&format=json"
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", url)
        resp = conn.getresponse()
        if resp.status == 200:
            data = resp.read()
            json_data = json.loads(data.decode("utf-8"))
            location = json_data["display_name"]
        conn.close()
        return location

    def get_forecast(self, latitude, longitude):
        forecast = None
        host = "api.openweathermap.org"
        api_key = "bef8f34daa67541b953d6ec4d58a0e62"
        url = "/data/2.5/weather" \
            f"?lat={latitude}&lon={longitude}&appid={api_key}&units=imperial"
        conn = http.client.HTTPConnection(host)
        conn.request("GET", url)
        resp = conn.getresponse()
        if resp.status == 200:
            data = resp.read()
            json_data = json.loads(data.decode("utf-8"))
            forecast = {
                "temp": json_data["main"]["temp"],
                "place": json_data["name"],
                "description": json_data["weather"][0]["description"],
                "wind_speed": json_data["wind"]["speed"]
            }
        conn.close()
        return forecast