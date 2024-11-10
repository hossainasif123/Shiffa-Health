from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_websocket_notification(user, message, event_type='notification'):
    """
    Utility function to send a WebSocket message to a user's notification group.
    It also saves the notification to the database for later retrieval and marks it as unread.
    """
    # Save the notification to the database, marked as unread
    Notification.objects.create(user=user, message=message, is_read=False)

    # Send the message to the user's WebSocket group (real-time notification)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{user.username}',  # Group name is based on username
        {
            'type': f'{event_type}_message',
            'message': message,
        }
    )
