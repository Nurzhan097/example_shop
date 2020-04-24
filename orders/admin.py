from django.contrib import admin
from . import models


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
	list_display = [
		'name',
		'is_active',
	]

class ProductInOrderInline(admin.TabularInline):
	model = models.ProductInOrder
	extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = [
		'customer_name',
		'customer_email',
		'customer_phone',
		'comments',
		'status',
		'is_active',
	]
	inlines = [ProductInOrderInline,]


@admin.register(models.ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
	list_display = [
		'order',
		'product',
		'price_per_item',
		'total_amount',
		'is_active',
	]


@admin.register(models.ProductInBasket)
class ProductInBasketAdmin(admin.ModelAdmin):
	list_display = [
		'product',
		'session_key',
		'order',
		'price_per_item',
		'total_amount',
		'is_active',
	]






















