import json
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer

from .models import Message
from .views import get_current_chat

User = get_user_model()

class ChatConsumer(WebsocketConsumer): 
    
    def new_message(self, data):
        # save message to database
        chat_object = get_current_chat(self.chat_id)
        author_username = data['from']
        author = User.objects.get(username=author_username)
        message = Message.objects.create(chat=chat_object, author=author, content=data['message'])
        # send message
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        self.send_chat_message(content)
        
    
    def fetch_messages(self, data):
        # fetch messages from database
        messages = Message.last_messages(chat_id=self.chat_id ,num=10)    
        # send messages  
        content = {
            'command': 'messages',
            'messages': self.json_list(messages)
        }
        self.send_messages(content)
        
    def json_list(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
        
    def message_to_json(self, message):       
        return {
            "id": message.id,
            "author": message.author.username,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
        }
        
    commands = {
        'fetch_messages' : fetch_messages,
        'new_message' : new_message
    }
          
    def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_group_name = "chat_%s" % self.chat_id
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name, self.channel_name
        )       
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)
        
    # Send messages to WebSocket
    def send_messages(self, content):
        self.send(text_data=json.dumps(content))
    
    # Send message to room group   
    def send_chat_message(self, content):
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name, 
            {
                'type': 'chat_message',
                'content': content
            }
        )

    # Send message to WebSocket
    def chat_message(self, event):
        self.send(text_data=json.dumps(event['content']))
        
 