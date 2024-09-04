import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from notificaciones.models import Notification, TypeNotification

class ChatConsumer(WebsocketConsumer):
    def connect(self):
    # accept connection
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat{self.id}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    # receive message from WebSocket
    def receive(self, text_data):
        user = self.scope['user']
        #print(user)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username
            }
        )
        # send message to WebSocket
        #self.send(text_data=json.dumps({'message': message}))
    def chat_message(self,event):        
        self.send(text_data=json.dumps(event))


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
    # accept connection        
        self.group_name = 'notifications'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
    # receive message from WebSocket
    def receive(self, text_data):
        #user = self.scope['user']
        text_data_json = json.loads(text_data)
        notification = text_data_json['notification']
        print(notification)
        user = self.scope['user']
        notification_ = Notification(
            detalle=notification['detalle'],
            user=user,
            type=TypeNotification.objects.get(pk=notification['type']) 
            )
        notification_.save()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'send_notification',
                'notification': {
                    'detalle':notification['detalle'],
                    'type':TypeNotification.objects.get(pk=notification['type']).type
                },
            }
        )
    def send_notification(self,event):        
        self.send(text_data=json.dumps(event))