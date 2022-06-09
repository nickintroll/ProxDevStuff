from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):

	def __init__(self, request):
		self.session = request.session
		
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		
		self.cart = cart
	

	def add(self, product, quantity=1, override_quantity=False):
		
		prod_id = str(product.id)
		if prod_id not in self.cart:
			self.cart[prod_id] = {
				'quantity': 0,
				'price': str(product.price)
			}
		print(self.cart)

		if override_quantity:
			self.cart[prod_id]['quantity'] = quantity
		
		else:
			self.cart[prod_id]['quantity'] += quantity

		self.save()


	def save(self):
		self.session.modified = True


	def remove(self, product):
		prod_id = str(product.id)
		if prod_id in self.cart:
			del self.cart[prod_id]
			self.save()


	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)

		cart = self.cart.copy()
		for prod in products:
			cart[str(prod.id)]['product'] = prod
		
		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['quantity'] * item['price']
			
			yield item
	
	
	def ___len__(self):
		return sum(item['quntity'] for item in self.cart.values())

	
	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	
	def clear(self):
		self.session[settions.CART_SESSION_ID]
		self.save()
