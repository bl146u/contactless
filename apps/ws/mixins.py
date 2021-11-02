from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ConsumerMixin(AsyncJsonWebsocketConsumer):
    _group: str
    _channel: str

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self._group,
            self._channel,
        )
