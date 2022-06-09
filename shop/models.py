from django.db import models
from users.models import Profile 
from django.shortcuts import reverse


class Product(models.Model):
	# relationship
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products_created')

	# initializatoin
	name		= models.CharField(max_length=50, db_index=True)
	slug		= models.SlugField(max_length=60, db_index=True, unique=True)
	description	= models.TextField()
	price		= models.DecimalField(max_digits=10, decimal_places=2)
	available	= models.BooleanField(default=True)

	# timestuff
	created		= models.DateTimeField(auto_now_add=True)
	upfated		= models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('created', 'name')


	def __str__(self):
		return self.name


	def get_absolute_url(self):
		return reverse("shop:product_detail", kwargs={"slug": self.slug})


class Image(models.Model):
	product = models.ForeignKey(Product, default=None, related_name='images', on_delete=models.CASCADE)
	file = models.ImageField(upload_to='products/%Y%m%d')
