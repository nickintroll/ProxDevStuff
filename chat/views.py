from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import Chat

@login_required
def chat_room(request, slug):
	chat = get_object_or_404(Chat, slug=slug)
	return render(request, 'chat_room.html', {'chat': chat})


@login_required
def get_chat_room(request, user2):

	chat = None
	user1 = request.user.profile
	user2 = get_object_or_404(Profile, id=user2)

	
	chat = Chat.objects.filter(
		member_accepted=user2, 
		member_started=user1)

	if list(chat) != []:

		chat = chat[0]
	else:

		chat = Chat.objects.filter(
			member_accepted=user1, 
			member_started=user2)
		
		if list(chat) != []:
		
			chat = chat[0]
		else:
		
			chat = Chat.objects.create(
				member_started=user1, 
				member_accepted=user2,
				slug=f'{user1.id}{user2.id}'
				)

	return redirect('chat:chat_room', chat.slug)