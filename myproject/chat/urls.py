from django.urls import path

from . import views

app_name = 'chat'

# 'chat/'
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:chat_id>/", views.room_by_chat, name="room_by_chat"),
    path("user/<int:user_id>/", views.room_by_user, name="room_by_user"),
]