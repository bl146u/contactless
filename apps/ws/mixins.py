from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ConsumerMixin(AsyncJsonWebsocketConsumer):
    group_name: str
    channel_name: str

    async def connect(self, **kwargs):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
