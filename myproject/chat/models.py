from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author}: {self.content}'
    
    def last_messages(num):
        return Message.objects.order_by('created_at').all()[:num]
        