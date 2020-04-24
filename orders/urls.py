from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('', views.main, name='main'),
	path('basket/adding/', views.basket_adding, {'act': 'add', }, name='basket_adding'),
	path('basket/delete/', views.basket_adding, {'act': 'delete', },  name='basket_delete'),
	path('checkout/', views.checkout,  name='checkout'),
]