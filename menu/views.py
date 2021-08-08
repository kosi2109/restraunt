from django.shortcuts import render,redirect
from .models import *
from datetime import date
from django.http import JsonResponse
import json
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login, logout

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
			messages.info(request,'Username or Password is incorrect..')
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
		user = request.user.muser
		order = list(user.order_set.all())
		if len(order) > 0:
			last_order = order[-1]
			if last_order.ckecked == False:
				current_order = last_order
				order_item = current_order.orderitem_set.all()
			else:
				current_order = None
				order_item = []
		else:
			current_order = None
			order_item = []
	else:
		order = []
		current_order = None
		order_item = []

	

	ctx = {'menu':menu,'category':category,'order_item':order_item,'current_order':current_order}
	return render(request , 'menu/menu.html',ctx)

def category(request,slug):
	category = Category.objects.all()
	ct = Category.objects.get(slug=slug)
	menu = Menu.objects.filter(category=ct)
	if request.user.is_authenticated:
		user = request.user.muser
		order = list(user.order_set.all())
		if len(order) > 0:
			last_order = order[-1]
			print(last_order)
			if last_order.ckecked == False:
				current_order = last_order
				order_item = current_order.orderitem_set.all()
			else:
				current_order = None
				order_item = []
		else:
			current_order = None
			order_item = []
	else:
		order = []
		current_order = None
		order_item = []


	ctx = {'menu':menu,'category':category,'order_item':order_item,'current_order':current_order}
	return render(request , 'menu/category.html',ctx)



def handleOrder(request):
	if request.user.is_authenticated:
		user = request.user.muser
		order = list(user.order_set.all())
		data = json.loads(request.body)
		menuSlug = data['menuSlug']
		action = data['action']
		item = Menu.objects.get(slug=menuSlug)
		if len(order) > 0 :
			last_order = order[-1]
			if action == 'add':
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
				
		else:
			new = Order.objects.create(user=user)
			OrderItem.objects.create(order=new,item=item)
	
	return JsonResponse(data)

def checkout(request,slug):
	user = request.user.muser
	order = Order.objects.get(user=user,slug=slug)
	item = order.orderitem_set.all()
	if request.method == 'POST':
		order.ckecked = True
		order.save()
		return redirect('menu:menu')
	ctx = {'order':order,'item':item}
	return render(request , 'menu/checkout.html',ctx)


def search(request):
	category = Category.objects.all()
	menu = Menu.objects.all()
	
	if request.user.is_authenticated:
		user = request.user.muser
		order = list(user.order_set.all())
		if len(order) > 0:
			last_order = order[-1]
			if last_order.ckecked == False:
				current_order = last_order
				order_item = current_order.orderitem_set.all()
			else:
				current_order = None
				order_item = []
		else:
			current_order = None
			order_item = []
	else:
		order = []
		current_order = None
		order_item = []

	if request.method == "POST":
		data = request.POST['searched']
		menu = Menu.objects.filter(name__icontains=data)
		if len(data) > 0:
			ctx = {'menu':menu,'category':category,'order_item':order_item,'current_order':current_order,'data':data}
			return render(request,'menu/search.html',ctx)
		else:
			return redirect('menu:menu')
	else:
		ctx = {'category':category,'order_item':order_item,'current_order':current_order}
		return render(request,'menu/search.html',ctx)
