from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('', views.main_page, name='main_page'),
	path('<slug:category_slug>/<slug:product_slug>/<int:product_id>/', views.product_detail, name='product_detail'),
]