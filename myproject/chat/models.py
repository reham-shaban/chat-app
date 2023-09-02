from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()

REACTIONS = (
    (1, 'like'), (2, 'love'), (3, 'haha'), (4, 'wow'), (5, 'sad'), (6, 'angry')
)

TYPE = (
    ('text', 'Text'), ('image', 'Image'), ('voice_record', 'Voice Record')
)

# models
class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name='user1', null=True, on_delete=models.SET_NULL)
    user2 = models.ForeignKey(User, related_name='user2', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user1} - {self.user2}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='author', null=True, on_delete=models.SET_NULL)
    message_type = models.CharField(max_length=20, choices=TYPE)
    text = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    voice_record = models.FileField(upload_to='voice_records/', blank=True, null=True, validators=[FileExtensionValidator(['wav', 'mp3'])])
    reaction = models.IntegerField(blank=True, null=True, choices=REACTIONS)
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author}: {self.message_type} "{self.text}"'
    
    def last_messages(chat_id, num):
        chat = Chat.objects.get(pk=chat_id)
        return Message.objects.filter(chat=chat)[:num]
        
