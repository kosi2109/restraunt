from django.shortcuts import render,redirect
from .models import *
from datetime import date
from django.http import JsonResponse
import json
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from table.models import *
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','first_name','last_name','password1','password2']
		widgets = {
			'username': forms.TextInput(attrs={'id':'username','placeholder':'Username'}),
			'email': forms.TextInput(attrs={'id':'exampleInputEmail1','placeholder':'Email'}),
			'password1': forms.PasswordInput(attrs={'id':'Password1'}),
			'password2': forms.PasswordInput(attrs={'id':'Password2'}),
			'first_name': forms.TextInput(attrs={'placeholder':'First Name'}),
			'last_name': forms.TextInput(attrs={'placeholder':'Last Name'}),
		}

def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			email = form.cleaned_data.get('email')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			phone = request.POST.get('phone')
			address = request.POST.get('address')
			MUser.objects.create(
				user = user ,
				F_Name = first_name,
				L_Name = last_name,
				email = email,
				phone = phone,
				address=address
				)
			return redirect('menu:userLogin')


	ctx = {'form':form}
	return render(request,'menu/signup.html',ctx)



def userLogin(request):
	if request.method == 'POST' or None:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('menu:menu')
		else:
			return redirect('menu:userLogin')

	return render(request ,'menu/login.html' )

def userLogout(request):
	logout(request)
	return redirect('menu:menu')

def home(request):
	return render(request , 'menu/index.html')

def menu(request):
	category = Category.objects.all()
	menu = Menu.objects.all()
	if request.user.is_authenticated:
		if not request.user.is_table:
			user = request.user.muser
			order = list(user.order_set.all())
			if len(order) > 0:
				last_order = order[0]
				if last_order.ckecked == False:
					current_order = last_order
					order_item = current_order.orderitem_set.all()
					cart_item = []
				else:
					current_order = None
					order_item = []
					cart_item = []
			else:
				current_order = None
				order_item = []
				cart_item = []
		else:
			user = request.user.table
			order = list(user.tableorder_set.all())
			if len(order) > 0:
				last_order = order[0]
				if last_order.ckecked == False:
					current_order = last_order
					order_item = current_order.tableorderitem_set.filter(ordered=True)
					cart_item = current_order.tableorderitem_set.filter(ordered=False)
				else:
					current_order = None
					order_item = []
					cart_item = []
			else:
				current_order = None
				order_item = []
				cart_item = []
	else:
		order = []
		current_order = None
		order_item = []
		cart_item = []

	

	ctx = {'menu':menu,'category':category,'order_item':order_item,'current_order':current_order,'cart_item':cart_item}
	return render(request , 'menu/menu.html',ctx)

def category(request,slug):
	category = Category.objects.all()
	ct = Category.objects.get(slug=slug)
	menu = Menu.objects.filter(category=ct)
	if request.user.is_authenticated:
		if not request.user.is_table:
			user = request.user.muser
			order = list(user.order_set.all())
			if len(order) > 0:
				last_order = order[0]
				print(last_order)
				if last_order.ckecked == False:
					current_order = last_order
					order_item = current_order.orderitem_set.all()
					cart_item = []
				else:
					current_order = None
					order_item = []
					cart_item = []
			else:
				current_order = None
				order_item = []
				cart_item = []
		else:
			user = request.user.table
			order = list(user.tableorder_set.all())
			if len(order) > 0:
				last_order = order[0]
				if last_order.ckecked == False:
					current_order = last_order
					order_item = current_order.tableorderitem_set.filter(ordered=True)
					cart_item = current_order.tableorderitem_set.filter(ordered=False)
				else:
					current_order = None
					order_item = []
					cart_item = []
			else:
				current_order = None
				order_item = []
				cart_item = []
	else:
		order = []
		current_order = None
		order_item = []
		cart_item = []

	ctx = {'menu':menu,'category':category,'order_item':order_item,'current_order':current_order,'cart_item':cart_item}
	return render(request , 'menu/category.html',ctx)



def handleOrder(request):
	if request.user.is_authenticated:
		if not request.user.is_table:
			user = request.user.muser
			order = list(user.order_set.all())
			data = json.loads(request.body)
			action = data['action']
			if len(order) > 0 :
				last_order = order[0]
				if action == 'add':
					menuSlug = data['menuSlug']
					item = Menu.objects.get(slug=menuSlug)
					if last_order.ckecked == False:
						if OrderItem.objects.filter(order=last_order,item=item).exists():
							ordered_item = OrderItem.objects.get(order=last_order,item=item)
							ordered_item.quatity += 1
							ordered_item.save()
						else:
							OrderItem.objects.create(order=last_order,item=item)
					else:
						new = Order.objects.create(user=user)
						OrderItem.objects.create(order=new,item=item)

				if action == 'increase':
					menuSlug = data['menuSlug']
					item = OrderItem.objects.get(id=menuSlug)
					item.quatity += 1
					item.save()

				if action == 'decrease':
					menuSlug = data['menuSlug']
					item = OrderItem.objects.get(id=menuSlug)
					item.quatity -= 1
					item.save()
					if item.quatity < 1:
						item.delete()
					
			else:
				new = Order.objects.create(user=user)
				OrderItem.objects.create(order=new,item=item)

		else:
			user = request.user.table
			order = list(user.tableorder_set.all())
			data = json.loads(request.body)
			
			action = data['action']
			
			if len(order) > 0 :
				last_order = order[0]
				if action == 'add':
					menuSlug = data['menuSlug']
					item = Menu.objects.get(slug=menuSlug)
					if last_order.ckecked == False:
						if TableOrderItem.objects.filter(order=last_order,item=item,ordered=False).exists():
							ordered_item = TableOrderItem.objects.get(order=last_order,item=item,ordered=False)
							ordered_item.quatity += 1
							ordered_item.save()
						else:
							TableOrderItem.objects.create(order=last_order,item=item)
					else:
						new = TableOrder.objects.create(user=user)
						TableOrderItem.objects.create(order=new,item=item)
				if action == 'comfirm':
					not_ordered = TableOrderItem.objects.filter(order=last_order,ordered=False)
					ordered = TableOrderItem.objects.filter(order=last_order,ordered=True)
					if len(ordered) > 0:
						for i in not_ordered:
							for j in ordered:
								print(i,j,'sadasd')
								if i.item.slug == j.item.slug:
									j.quatity += i.quatity
									j.save()
									i.delete()
									

						not_ordered = TableOrderItem.objects.filter(order=last_order,ordered=False)
						for i in not_ordered:
							i.ordered = True
							i.save()

					else:
						for i in not_ordered:
							i.ordered = True
							i.save()

				if action == 'increase':
					menuSlug = data['menuSlug']
					item = TableOrderItem.objects.get(id=menuSlug)
					item.quatity += 1
					item.save()

				if action == 'decrease':
					menuSlug = data['menuSlug']
					item = TableOrderItem.objects.get(id=menuSlug)
					item.quatity -= 1
					item.save()
					if item.quatity < 1:
						item.delete()

			else:
				new = TableOrder.objects.create(user=user)
				TableOrderItem.objects.create(order=new,item=item)

	
	return JsonResponse(data)

def checkout(request,slug):
	if not request.user.is_table:
		user = request.user.muser
		order = Order.objects.get(user=user,slug=slug)
		item = order.orderitem_set.all()
		if request.method == 'POST':
			
			order.order_date = datetime.now().date()
			order.order_time = datetime.now().time()
			order.ckecked = True
			order.save()
			return redirect('menu:menu')
		
	else:
		user = request.user.table
		order = TableOrder.objects.get(user=user,slug=slug)
		item = order.tableorderitem_set.filter(ordered=True)
		if request.method == 'POST':
			
			order.order_date = datetime.now().date()
			order.order_time = datetime.now().time()
			order.ckecked = True
			order.save()
			logout(request)
			return redirect('menu:menu')

	ctx = {'order':order,'item':item}
	return render(request , 'menu/checkout.html',ctx)


def search(request):
	category = Category.objects.all()
	menu = Menu.objects.all()
	
	if request.user.is_authenticated:
		if not request.user.is_table:
			user = request.user.muser
			order = list(user.order_set.all())
			if len(order) > 0:
				last_order = order[0]
				if last_order.ckecked == False:
					current_order = last_order
					order_item = current_order.orderitem_set.all()
					cart_item = []
				else:
					current_order = None
					order_item = []
					cart_item = []
			else:
				current_order = None
				order_item = []
				cart_item = []
		else:
			user = request.user.table
			order = list(user.tableorder_set.all())
			if len(order) > 0:
				last_order = order[0]
				if last_order.ckecked == False:
					current_order = last_order
					order_item = current_order.tableorderitem_set.filter(ordered=True)
					cart_item = current_order.tableorderitem_set.filter(ordered=False)
				else:
					current_order = None
					order_item = []
					cart_item = []
			else:
				current_order = None
				order_item = []
				cart_item = []
	else:
		order = []
		current_order = None
		order_item = []
		cart_item = []

	if request.method == "POST":
		data = request.POST['searched']
		menu = Menu.objects.filter(name__icontains=data)
		if len(data) > 0:
			ctx = {'menu':menu,'category':category,'order_item':order_item,'current_order':current_order,'data':data}
			return render(request,'menu/search.html',ctx)
		else:
			return redirect('menu:menu')
	else:
		ctx = {'category':category,'order_item':order_item,'current_order':current_order,'cart_item':cart_item}
		return render(request,'menu/search.html',ctx)


def orderHistory(request):
	if not request.user.is_table:
		user = request.user.muser
		order = Order.objects.filter(user=user,ckecked=True)
		totalorder = len(order)
		ctx = {'order':order,'totalorder':totalorder,'user':user}
		return render(request,'menu/history.html',ctx)


def jointable(request):

	return render(request,'menu/tableRequest.html')