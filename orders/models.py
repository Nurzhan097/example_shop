from django.db import models
from django.db.models import signals

from products import models as product_models


class Status(models.Model):
	name = models.CharField(max_length=30, )

	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return f'Status {self.name}'

	class Meta:
		verbose_name = 'Статус'
		verbose_name_plural = 'Статусы'


# Заказы
class Order(models.Model):
	customer_name = models.CharField(max_length=120, blank=True, null=True, default=None)
	customer_email = models.EmailField( blank=True, null=True, default=None)
	customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
	customer_address = models.CharField(max_length=255, blank=True, null=True, default=None)
	comments = models.TextField(blank=True, null=True, default=None)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	status = models.ForeignKey(Status, on_delete=models.CASCADE)

	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return f'Order {self.id}, to {self.customer_name}, status {self.status.name}'

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'


# продукты в заказе
class ProductInOrder(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None)
	product = models.ForeignKey(product_models.Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
	nmb = models.IntegerField(default=1)
	price_per_item = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)

	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return f'Product {self.product.name} in order {self.order.id}'

	class Meta:
		verbose_name = 'Продукт в заказе'
		verbose_name_plural = 'Продукты в заказах'

	def save(self, *args, **kwargs):
		price_per_item = self.product.price
		total_amount = self.nmb * price_per_item
		self.total_amount = total_amount
		self.price_per_item = price_per_item

		super(ProductInOrder, self).save(*args, **kwargs)


# функция для вып опер после сохранения
def product_in_order_post_save(sender, instance, created, **kwargs):
	order = instance.order
	all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

	order_total_price = 0
	for item in all_products_in_order:
		order_total_price += item.total_amount

	instance.order.total_price = order_total_price
	instance.order.save(force_update=True)


# Вызов функции для модели ProductInOrder
signals.post_save.connect(product_in_order_post_save, sender=ProductInOrder)



# Продукт в корзине
class ProductInBasket(models.Model):
	session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None)
	product = models.ForeignKey(product_models.Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
	nmb = models.IntegerField(default=1)
	price_per_item = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)

	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return f'Product {self.product.title} '

	class Meta:
		verbose_name = 'Продукт в корзине '
		verbose_name_plural = 'Продукты в корзине'

	def save(self, *args, **kwargs):
		price_per_item = self.product.price
		self.price_per_item = price_per_item
		self.total_amount = int(self.nmb) * price_per_item
		# self.total_amount = total_amount
		super(ProductInBasket, self).save(*args, **kwargs)











