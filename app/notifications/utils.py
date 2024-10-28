from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_real_time_notification(user_id, notification_type, message):
    channel_layer = get_channel_layer()
    group_name = f'notifications_{user_id}'

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'message': {
                'type': notification_type,
                'message': message,
            }
        }
    )