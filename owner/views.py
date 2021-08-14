from django.shortcuts import render,redirect
from table.models import TableOrder
from menu.models import Order,MUser,Menu,Category
# Create your views here.
from datetime import datetime, timedelta
import operator
from django.db.models import Q
from .forms import *
from django.http import JsonResponse
import json
from .filters import OrderFilter,MenuFilter
from .decorators import *
from django.contrib.auth.decorators import login_required


class Sales:
	def __init__(self,order,table):
		self.order = order
		self.table = table

	def dalySale(self):
		today = datetime.now().date()
		order = self.order.objects.filter(ckecked = True,order_date=today)
		table = self.table.objects.filter(ckecked = True,order_date=today)
		total = 0
		for i in order:
			total += i.get_order_total
		for i in table:
			total += i.get_order_total
		return total

	def monthlySale(self):
		dt = datetime.now().date()
		this_mo = dt.month
		nex_mo = dt.month +1
		timestamp_from = datetime(2021,this_mo,1)
		timestamp_to = datetime(2021,nex_mo,1)
		order = self.order.objects.filter(ckecked = True,order_date__range=[timestamp_from, timestamp_to])
		table = self.table.objects.filter(ckecked = True,order_date__range=[timestamp_from, timestamp_to])
		total = 0
		for i in order:
			total += i.get_order_total
		for i in table:
			total += i.get_order_total
		return total

	def yearSale(self):
		dt = datetime.now().date()
		this_mo = dt.year
		nex_mo = dt.year +1
		timestamp_from = datetime(this_mo,1,1)
		timestamp_to = datetime(nex_mo,1,1)
		order = self.order.objects.filter(ckecked = True,order_date__range=[timestamp_from, timestamp_to])
		table = self.table.objects.filter(ckecked = True,order_date__range=[timestamp_from, timestamp_to])
		total = 0
		for i in order:
			total += i.get_order_total
		for i in table:
			total += i.get_order_total
		return total

class MostCommonUser():

	def most_order():
		users = MUser.objects.all()
		li = {}
		for index,i in enumerate(users):
			orders = i.get_total_order
			li[index] = orders

		sorted_li = sorted(li.items(), key=operator.itemgetter(1),reverse=True)
		most_order_user = []
		for i in sorted_li[0:5]:
			ind = i[0]
			user = MUser.objects.all()
			most_order_user.append(users[ind])
		return most_order_user

	def most_money_spend():
		users = MUser.objects.all()
		li = {}
		for index,i in enumerate(users):
			orders = i.get_total_spend
			li[index] = orders

		sorted_li = sorted(li.items(), key=operator.itemgetter(1),reverse=True)
		most_order_user = []
		for i in sorted_li[0:5]:
			ind = i[0]
			user = MUser.objects.all()
			most_order_user.append(users[ind])
		return most_order_user

class BestMenu():
	def get_best_item():
		menu = Menu.objects.all()
		li = {}
		for index,i in enumerate(menu):
			itemtotal = i.get_total_selling
			li[index] = itemtotal

		sorted_li = sorted(li.items(), key=operator.itemgetter(1),reverse=True)
		most_order_item = []
		for i in sorted_li[0:5]:
			ind = i[0]
			menu = Menu.objects.all()
			most_order_item.append(menu[ind])
		return most_order_item

	def get_best_cate():
		cate = Category.objects.all()
		li = {}
		for index,i in enumerate(cate):
			
			catetotal = i.get_total_selling
			li[index] = catetotal

		sorted_li = sorted(li.items(), key=operator.itemgetter(1),reverse=True)
		most_order_cate = []
		for i in sorted_li[0:5]:
			ind = i[0]
			cate = Category.objects.all()
			most_order_cate.append(cate[ind])
		return most_order_cate
		

@admin_only
@login_required(login_url='menu:login')
def home(request):
	sale = Sales(Order,TableOrder)
	year = sale.yearSale()
	month = sale.monthlySale()
	daily = sale.dalySale()
	sales = dict(year=year,month=month,daily=daily)

	most_order = MostCommonUser.most_order()
	most_spent = MostCommonUser.most_money_spend()
	most_order_item = BestMenu.get_best_item()
	most_order_cate = BestMenu.get_best_cate()

	ctx = {'sales':sales,'most_order':most_order,'most_spent':most_spent,'most_order_item':most_order_item,'most_order_cate':most_order_cate,'nav':'home'}
	return render(request,'owner/index.html',ctx)

@admin_only
@login_required(login_url='menu:login')
def order(request):
	filterform = OrderFilter()
	today = datetime.now().date()
	activeorders = []
	allorders = []
	activeorder = Order.objects.filter(Q(status='Cooking',ckecked=True) | Q(status='Delivering',ckecked=True))
	completeorder = Order.objects.filter(status='Delivered',ckecked=True,order_date=today)
	activetableorder = TableOrder.objects.filter(ckecked=False)
	completetableorder = TableOrder.objects.filter(ckecked=True,order_date=today)

	for i in activeorder:
		activeorders.append(i)

	for i in activetableorder:
		activeorders.append(i)

	for i in completeorder:
		allorders.append(i)

	for i in completetableorder:
		allorders.append(i)
	
	ctx = {'allorders':allorders,'activeorders':activeorders,'filterform':filterform,'nav':'order'}
	return render(request,'owner/orders.html',ctx)

@admin_only
@login_required(login_url='menu:login')
def menu(request):
	category = Category.objects.all()
	menu = Menu.objects.all()
	menuform = MenuForm()
	menufilter = MenuFilter()
	if request.method == "POST":
		menuform = MenuForm(request.POST,request.FILES)
		if menuform.is_valid():
			menuform.save()
			return redirect('owner:menu')
		else:
			menuform = MenuForm()
	if request.method == "GET":
		menufilter = MenuFilter(request.GET,queryset=menu)
		menu = menufilter.qs

	ctx ={'category':category,'menu':menu,'menuform':menuform,'menufilter':menufilter,'nav':'menu'}
	return render(request,'owner/menu.html',ctx)

@admin_only
@login_required(login_url='menu:login')
def addcategory(request):
	if request.method == "POST":
		name = request.POST.get('category')
		image = request.FILES.get('image')
		Category.objects.create(name=name,image=image)

	return redirect('owner:menu')


@admin_only
@login_required(login_url='menu:login')
def menuDelete(request,slug):
	item = Menu.objects.get(slug=slug)
	if request.method == "POST":
		item.delete()
		return redirect('owner:menu')
	return render(request,'owner/delete.html',{'item':item,'nav':'menu'})



@admin_only
@login_required(login_url='menu:login')
def cateDelete(request,slug):
	item = Category.objects.get(slug=slug)
	if request.method == "POST":
		item.delete()
		return redirect('owner:menu')
	return render(request,'owner/delete.html',{'item':item,'nav':'menu'})



@admin_only
@login_required(login_url='menu:login')
def statusControl(request):
	data = json.loads(request.body)
	orderSlug = data['order']
	value = data['value']
	
	order = Order.objects.get(slug=orderSlug)

	order.status = value
	order.save()


	return JsonResponse(data)


@admin_only
@login_required(login_url='menu:login')
def filterorder(request):
	order = Order.objects.all()
	filterform = OrderFilter(request.GET,queryset=order)
	order = filterform.qs
	ctx = {'order':order,'nav':'order'}


	return render(request,'owner/filter.html',ctx)
