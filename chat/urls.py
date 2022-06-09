from django.urls import path
from .views import get_chat_room, chat_room

app_name = 'chat'

urlpatterns = [
	path('<int:user2>/', get_chat_room, name='get_chat'),
	path('room/<int:slug>/', chat_room, name='chat_room'),
]
