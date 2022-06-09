from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify


class Profile(models.Model):
	OFFERS_TYPES = (
		('Part time', 'part time'),
		('Full time', 'full time'),
		('Project', 'project')
	)

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	
	offer_is = 			models.CharField(choices=OFFERS_TYPES, max_length=10)
	present_company = 	models.CharField(max_length=50)
	photo = 		 	models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)

	slug = 			 	models.SlugField(max_length=200, unique=True, blank=True, null=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.user)
		super().save(*args, **kwargs)		

	def __str__(self):
		return 'P for ' + self.user.username
	

	def get_absolute_url(self):
		return reverse('account:profile_other', args=[self.slug])
