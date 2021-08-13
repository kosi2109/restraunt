import django_filters
from menu.models import Order,Menu
from django import forms

class OrderFilter(django_filters.FilterSet):
    order_id = django_filters.CharFilter(field_name='order_id',lookup_expr='icontains',widget=forms.TextInput(attrs={'placeholder':'Order Id','class':'form-control mb-3'}))
    order_date__gt = django_filters.DateFilter(field_name='order_date', lookup_expr='gte',widget=forms.TextInput(attrs={'class':'form-control mb-3','type':'date'}))
    order_date__lt = django_filters.DateFilter(field_name='order_date', lookup_expr='lte',widget=forms.TextInput(attrs={'class':'form-control mb-3','type':'date'}))

    class Meta:
        model = Order
        fields = ['order_id']

class MenuFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains',widget=forms.TextInput(attrs={'placeholder':'Name','class':'form-control me-2'}))
    
    class Meta:
        model = Order
        fields = ['name']