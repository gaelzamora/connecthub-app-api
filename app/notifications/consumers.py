import json
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models import Notification
from .serializers import NotificationSerializer
from channels.db import database_sync_to_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                f'notifications_{self.user.id}',
                self.channel_name
            )
            await self.accept
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                f'notifications_{self.user.id}',
                self.channel_name
            )

    async def receive(self, text_data):
        pass

    async def send_notifications(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps(notification))

    @database_sync_to_async
    def get_notification_data(self, notification_id):
        notification = Notification.objects.get(id=notification_id)

        return NotificationSerializer(notification).data