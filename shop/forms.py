from django import forms
from .models import Product, Image


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'price', 'description', 'available')


class SearchForm(forms.Form):
	query = forms.CharField(max_length=30)


class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('file')

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
