from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector

from cart.forms import CartAddProductForm
from .forms import ProductForm, SearchForm
from .models import Product


def shop_main(request):
	form = SearchForm()
	products = Product.objects.all().order_by('-created')[:30]
	
	return render(request, 'main_page.html', {'prods': products, 'form': form})


def product_detail(request, slug):
	product = Product.objects.get(slug=slug)
	cart_add_form = CartAddProductForm()
	return render(request, 'detail.html', {'prod': product, 'cart_add_form': cart_add_form})


@login_required
def create_product(request):
	if request.method == 'POST':
		
		form = ProductForm(request.POST)
		if form.is_valid():
			product = form.save(commit=False)
			product.owner = request.user.profile
			product.slug = product.name + str(product.price)
			product.slug = product.slug.replace(' ', '_').replace('.', '')
			product.save()

		return redirect('shop:main_page')
	else:
		form = ProductForm()

	return render(request, 'form.html', {'form': form})


def search_product(request):
	form = SearchForm()
	query = None
	results = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			results = Product.objects.annotate(
				search=SearchVector(
					'name', 'description', 'owner__user__username','owner__present_company',  
				)
			).filter(search=query)
	
	return render(request, 'search.html', {
		'form':form,
		'query':query,
		'results': results
	})