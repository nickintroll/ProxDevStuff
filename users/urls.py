from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'account'
urlpatterns = [
	path('login/', views.login_page, name='login'),
	path('logout', LogoutView.as_view(), name='logout'), 

	path('registration/', views.register_page, name='registration'),
	path('me/', views.profile_me, name='profile_me'),
	path('update_me/', views.edit_profile, name='profile_edit'),
	path('users/', views.users, name='profiles_list'),
	path('search/', views.user_search, name='user_search'),
	path('<slug:user>/', views.profile_other,  name='profile_other'),
]