from django.db import models


# Категория
class Category(models.Model):
	title = models.CharField(max_length=80)
	slug = models.SlugField(unique=True, db_index=True)
	# prepopulated_fields = {"slug": ("title",)}
	image = models.ImageField(upload_to='category_images', blank=True, null=True, default=None )

	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return f'Category {self.title}'

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def get_url(self):
		return f'/{self.slug}/'


# Акции и скидки
class Discount(models.Model):
	title = models.CharField(max_length=80)
	slug = models.SlugField(unique=False, db_index=True)
	discount_percentage = models.IntegerField()
	image = models.ImageField(upload_to='discount_images', blank=True, null=True, default=None)

	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return f'Discount {self.title}'

	class Meta:
		verbose_name = 'Акции и скидки'
		verbose_name_plural = 'Акции и скидки'

	def get_url(self):
		return f'/{self.slug}/'


# Продукт
class Product(models.Model):
	FOR_WHOM = [
		('Female', "Женский"),
		('Male', "Мужской"),
		# ('Children', "Детская"),
		# ('Female', "Женский"),
	]

	title = models.CharField(max_length=120)
	slug = models.SlugField(db_index=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	for_whom = models.CharField(max_length=10, choices=FOR_WHOM, default='Female')
	discount = models.ForeignKey(Discount, on_delete=models.CASCADE,  blank=True, null=True, default=None)
	short_description = models.CharField(max_length=120, blank=True, null=True, default=None)
	description = models.TextField(blank=True, null=True, default=None)
	# number_of_clothes_size_s =

	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return f'Product {self.title}'

	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'

	def get_url(self):
		return f'/{self.category.slug}/{self.slug}/{self.id}/'


# Изображения продукта
class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
	image = models.ImageField(upload_to='product_images', )
	is_main = models.BooleanField(default=False)

	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return f'Изображения продукта {self.product.title}'

	class Meta:
		verbose_name = 'Изображения продукта'
		verbose_name_plural = 'Изображения продукта'

	def save(self, *args, **kwargs):
		if self.is_main is True:
			try:
				product_image_is_main = ProductImage.objects.get(product=self.product, is_main=True, is_active=True)
				product_image_is_main.is_main = False
				product_image_is_main.save()
			except ProductImage.DoesNotExist:
				pass

		if self.is_main is False:
			try:
				product_images = ProductImage.objects.get(product=self.product, is_main=True, is_active=True)
			except ProductImage.DoesNotExist:
				self.is_main = True
		super(ProductImage, self).save(*args, **kwargs)


# hero section
class HeroSection(models.Model):
	name = models.CharField(max_length=50)
	title = models.CharField(max_length=80)
	description = models.TextField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, default=None)
	discount = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True, default=None)
	banner_image = models.ImageField(upload_to='banner_images',)
	page_url = models.URLField()






