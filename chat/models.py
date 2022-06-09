from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from users.models import Profile


# Create your models here.
class Chat(models.Model):
	member_started = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chats_started')
	member_accepted = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chats_accepted')

	slug = models.SlugField(max_length=12, blank=True, null=True)


	def get_absolute_url(self):
		print('what')
		return reverse('chat:chat_room', args=[self.slug])


	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(f'{member_started.id}{member_accepted.id}')
		super().save(*args, **kwargs)


class ChatMessage(models.Model):
	sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
	
	message = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
