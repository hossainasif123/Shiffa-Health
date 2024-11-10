import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f'notifications_{self.scope["user"].username}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        event_type = text_data_json.get('event', 'notification')
        
        print(f"Received message: {message} with event type: {event_type}")  # Debugging output

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': f'{event_type}_message',
                'message': message,
            }
        )

    async def notification_message(self, event):
        message = event['message']
        print(f"Sending notification: {message}")  # Debugging output
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def booking_notification_message(self, event):
        message = event['message']
        print(f"Sending booking notification: {message}")  # Debugging output
        await self.send(text_data=json.dumps({
            'message': message
        }))


