from django.urls import path
from .views import *
app_name = 'menu'

urlpatterns =[
	path('signup/',registerPage ,name='registerPage'),
	path('login/',userLogin ,name='userLogin'),
	path('logout/',userLogout ,name='userLogout'),
	path('',home ,name='home'),
	path('menu/',menu ,name='menu'),
	path('handleOrder/',handleOrder ,name='handleOrder'),
	path('checkout/<slug:slug>',checkout ,name='checkout'),
	path('menu/<slug:slug>/',category ,name='category'),
	path('search/',search ,name='search'),
]