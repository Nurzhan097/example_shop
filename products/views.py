from django.shortcuts import render, get_object_or_404

# Create your views here.
from . import models


def main_page(request):
	products = models.Product.objects.filter(is_active=True)
	latest_products = models.Product.objects.filter(is_active=True).order_by('created')[:5]
	context = {
		'products': products,
		'latest_products': latest_products,
	}
	return render(request, 'products/main.html', context)


def product_detail(request, category_slug, product_slug, product_id):
	# TODO: Сделать поиск похожих товаров
	# RELATED PRODUCTS
	# Временно - последние
	latest_products = models.Product.objects.filter(is_active=True).order_by('created')[:5]

	product = get_object_or_404(models.Product, category__slug=category_slug, slug=product_slug, id=product_id, is_active=True)

	# Ключ сессии
	session_key = request.session.session_key
	if not session_key:
		request.session.cycle_key()
		print('key generated', request.session.session_key)
	print('key', request.session.session_key)

	context = {
		'related_products': latest_products,
		'product': product,
		'session_key': session_key,
	}
	return render(request, 'products/products_page.html', context)
