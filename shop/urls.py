from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
	path('', views.shop_main, name='main_page'),
	path('prod/<slug:slug>/', views.product_detail, name='product_detail'),
	path('create/', views.create_product, name='create_product'),
	path('search/', views.search_product, name='search_product'),
]