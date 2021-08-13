from django.urls import path
from .views import *
app_name = 'owner'

urlpatterns = [
	path('',home,name='home'),
	path('menu/',menu,name='menu'),
	path('order/',order,name='order'),
	path('addcategory/',addcategory,name='addcategory'),
	path('menuDelete/<slug:slug>/',menuDelete,name='menuDelete'),
	path('cateDelete/<slug:slug>/',cateDelete,name='cateDelete'),
	path('statusControl/',statusControl,name='statusControl'),
	path('filterorder/',filterorder,name='filterorder'),
]