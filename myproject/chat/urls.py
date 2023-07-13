from django.urls import path

from . import views

'chat/'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:chat_id>/", views.room_by_chat, name="room_by_chat"),
    path("user/<str:user_id>/", views.room_by_user, name="room_by_user"),
]