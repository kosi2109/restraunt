from django.urls import path
from .views import *
app_name = 'chef'

urlpatterns =[
	path('',orderView,name='orderView'),
	path('getOrders/',getOrders,name='getOrders'),
	path('cookControl/',cookControl,name='cookControl'),

]