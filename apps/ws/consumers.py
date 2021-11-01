import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MainConsumer(AsyncWebsocketConsumer):
    group_name: str = "tmp"
    channel_name: str = "tmp"

    async def connect(self):
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        name = text_data_json.get("name")
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "name": name,
                "message": message,
            },
        )

    async def chat_message(self, event):
        message = event.get("message")
        name = event.get("name")
        await self.send(
            text_data=json.dumps(
                {
                    "name": name,
                    "message": message,
                }
            )
        )
