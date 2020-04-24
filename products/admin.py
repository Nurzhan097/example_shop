from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = [
		'title',
		'slug',
		'image',
		'is_active',
	]
	prepopulated_fields = {"slug": ("title",)}


@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
	list_display = [
		'title',
		'slug',
		'discount_percentage',
		'image',
		'is_active',
	]
	prepopulated_fields = {"slug": ("title",)}


class ProductImageInline(admin.TabularInline):
	""""Для добавления изображения на странице продукта"""
	model = models.ProductImage
	extra = 0  # колличество авт созд полей


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = [
		'title',
		'slug',
		'price',
		'short_description',
		# 'description',
		'category',
		'for_whom',
		'is_active',
	]
	prepopulated_fields = {"slug": ("title",)}

	inlines = [ProductImageInline, ]  # подключение вложенной модели


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = [
		'product',
		'image',
		'is_active',
	]








