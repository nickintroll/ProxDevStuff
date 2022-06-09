from django.contrib.auth.models import User
from .models import Profile
from django import forms



class LoginForm(forms.Form):
	username = 		forms.CharField()
	password = 		forms.CharField(widget=forms.PasswordInput)



class RegistrationForm(forms.ModelForm):
	
	password1 = 		forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = 		forms.CharField(label='Repeat password', widget=forms.PasswordInput)


	OFFERS_TYPES = 		(
		('Part time', 'part time'),
		('Full time', 'full time'),
		('Project', 'project')
	)


	present_company = 	forms.CharField()
	offer_is = 			forms.TypedChoiceField(choices=OFFERS_TYPES)


	class Meta:
		model = User
		fields = ('username', 'email')

	def clean_password(self):
		cd = self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise forms.ValidationError('Password do\'t match.')
		else:
			return cd['password2']
		
		if len(cd['present_company']) > 50:
			raise forms.ValidationError('Too long company name.')


class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('offer_is', 'present_company')


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields =('username', 'email')


class SearchForm(forms.Form):
	query = forms.CharField()