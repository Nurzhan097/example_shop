from django.core.serializers import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from . import models


# Create your views here.
def main(request):
	pass


def basket_adding(request, act):
	if request.method == 'POST':
		data = request.POST
		message = ''

		# Ключ сессии
		session_key = request.session.session_key
		if not session_key:
			request.session.cycle_key()

		product_id = data.get("product_id")
		if act == 'add':
			# Добаление продукта в корзину
			nmb = data.get("nmb")
			new_product, created = models.ProductInBasket.objects.get_or_create(
				session_key=session_key,
				product_id=product_id,
				is_active = True,
				defaults={'nmb': nmb},
			)
			if not created:
				new_product.nmb += int(nmb)
				new_product.save(force_update=True)
				message = f'добаленно еще  {nmb} штук в {new_product.product.title}, и того {new_product.nmb}.'
			else:
				message = f'Товар был добавленн в вашу корзину'

		elif act == 'delete':
			# Удаление продукта (дезактивация)
			models.ProductInBasket.objects.filter(product_id=product_id, session_key=session_key, is_active=True).update(is_active=False)
			deleted_product_from_cart = models.ProductInBasket.objects.filter(product_id=product_id, session_key=session_key, is_active=False)
			message = f'Продукт {deleted_product_from_cart[0].product.title} удален из вашей корзины'

		# Продукты в корзине
		products_total_nmb = models.ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
		products_in_basket = models.ProductInBasket.objects.filter(session_key=session_key, is_active=True)
		products_in_basket_list = list()
		for item in products_in_basket:
			product_dict = dict()
			product_dict['id'] = item.product.id
			product_dict['title'] = item.product.title
			product_dict['nmb'] = item.nmb
			product_dict['price_per_item'] = item.price_per_item
			product_dict['total_amount'] = item.total_amount
			product_dict['url'] = item.product.get_url()
			product_dict['image_url'] = item.product.image.get(is_main=True).image.url
			products_in_basket_list.append(product_dict)

		data = {
			'products_total_nmb': products_total_nmb,
			'products_in_basket_list': products_in_basket_list,
			'message': message
		}
		return JsonResponse(data)


def checkout(request):
	# Ключ сессии
	session_key = request.session.session_key
	if not session_key:
		request.session.cycle_key()

	return render(request, 'orders/checkout.html')

