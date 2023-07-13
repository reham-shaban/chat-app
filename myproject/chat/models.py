from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', null=True, on_delete=models.SET_NULL)
    user2 = models.ForeignKey(User, related_name='user2', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user1} - {self.user2}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='author', null=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author}: {self.content}'
    
    def last_messages(chat_id, num):
        chat = Chat.objects.get(pk=chat_id)
        return Message.objects.filter(chat=chat)[:num]
        
