from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .forms import LoginForm, RegistrationForm, ProfileEditForm, UserEditForm, SearchForm
from .models import Profile



def login_page(request):
	message = ''

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(
				request,
				username = cd['username'],
				password = cd['password']
			)

			if user != None:
				if user.is_active:
					login(request, user)
					message = 'authenticated successfully'

					return redirect('account:profile_me')

				else:
					message = 'user is deleted'
			else:
				message = 'invalid login or password'
		else:
			message = 'wrong data'
	else:
		form = LoginForm()

	return render(request, 'users/login.html', {'form': form, 'message': message})


def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			new_user = form.save(commit=False)
			new_user.set_password(cd['password1'])
			new_user.save()

			Profile.objects.create(
				user = new_user,
				offer_is=cd['offer_is'],
				present_company=cd['present_company'] 
			)

			print(new_user)
			"""
				HERE SHOULD BE REDIRECT
			"""
		else:
			print('FUCK')
	else:
		form = RegistrationForm()
	return render(request, 'users/registration.html', {'form': form})


@login_required
def profile_me(request):
	profile = Profile.objects.get(user=request.user)
	chats = [i for i in profile.chats_started.all()]
	chats = [i for i in profile.chats_accepted.all() if i not in chats] + chats
	
	return render(request, 'profile/me.html', {'profile': profile, 'chats': chats})


def users(request):
	form = SearchForm()
	profiles = Profile.objects.all()
	return render(request, 'profile/users_list.html',  {'profiles':profiles, 'form':form})


def profile_other(request, user):
	prof = get_object_or_404(Profile, slug=user)
	return render(request, 'profile/other.html', {'profile':prof})


@login_required
def edit_profile(request):
	if request.method == "POST":
		user_form = UserEditForm(instance=request.user, data=request.POST)
		prof_form = ProfileEditForm(instance=request.user.profile, data=request.POST, 
																	files=request.FILES)
		if user_form.is_valid() and prof_form.is_valid():
			user_form.save()
			prof_form.save()
			return  redirect('account:profile_me')
	else:
		user_form = UserEditForm(instance=request.user)
		prof_form = ProfileEditForm(instance=request.user.profile)

	return render(request, 'profile/edit.html', {'user_form': user_form, 'profile_form': prof_form})


def user_search(request):
	form = SearchForm()
	query = None
	results = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			results = Profile.objects.annotate(
				search=SearchVector('present_company', 'user__username')
			).filter(search=query)

	return render(
		request, 'profile/users_search.html', 
		{
			'form':form, 
			'query':query, 
			'results':results
		}
		)