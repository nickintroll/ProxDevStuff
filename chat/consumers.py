from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, Chat
from asgiref.sync import  async_to_sync
from django.utils import timezone
import json


class ChatConsumer(AsyncWebsocketConsumer):

	@database_sync_to_async
	def relate_chat(self):
		self.chat_object = Chat.objects.get(slug=self.id)

	@database_sync_to_async
	def save_message(self, message, user):
		ChatMessage.objects.create(sender=user.profile, chat=self.chat_object, message=message)


	async def connect(self):

		self.user = self.scope['user']
		self.id = self.scope['url_route']['kwargs']['slug']
		self.room_chat_name = 'chat_' + self.id

		await self.relate_chat()

		await self.channel_layer.group_add(
			self.room_chat_name, 
			self.channel_name
		)

		# accept connection
		await self.accept()

		
	async def disconnect(self, close_code):

		# leave the room
		await self.channel_layer.group_discard(
			self.room_chat_name,
			self.channel_name
		)


	async def receive(self, text_data):

		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		time = timezone.now()

		# send message to room
		await self.save_message(message=message, user=self.user)

		await self.channel_layer.group_send(
			self.room_chat_name,
			{
				'message':message,
				'type': 'chat_message',
				'user': self.user.username,
				'datetime': time.isoformat(),
			}
		)
		

	async def chat_message(self, event):
		# send message to websocket
		await self.send(text_data=json.dumps(event))
