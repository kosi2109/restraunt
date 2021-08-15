from django.db import models
import uuid
from django.contrib.auth.models import User,AbstractUser,AbstractBaseUser,PermissionsMixin
from datetime import date
from datetime import datetime
from django.utils import timezone
from cloudinary.models import CloudinaryField

class UserNew(AbstractUser):
	is_table = models.BooleanField(default=False)
	is_user = models.BooleanField(default=True)
	is_chef = models.BooleanField(default=False)

class MUser(models.Model):
	user = models.OneToOneField(UserNew,on_delete=models.CASCADE)
	F_Name = models.CharField(max_length=50,null=True)
	L_Name = models.CharField(max_length=50,null=True)
	email = models.CharField(max_length=100,null=True)
	phone = models.CharField(max_length=100,null=True)
	address = models.TextField(blank=False)

	@property 
	def get_total_spend(self):
		orders = self.order_set.all()
		total = 0 
		for order in orders:
			total += order.get_order_total
		return total

	@property 
	def get_total_order(self):
		orders = self.order_set.count()
		
		return orders


	def __str__(self):
		return f"{self.F_Name} {self.L_Name}"

class Category(models.Model):
	image = CloudinaryField('image')
	name = models.CharField(max_length=100,null=True)
	slug = models.SlugField(null=True,blank=True,unique=True)

	def save(self,*args,**kwargs):
		if not self.slug:
			name = self.name.split(" ")
			name = ''.join(name)
			self.slug = f"c_{name.lower()}"
			count = 1
			while Category.objects.filter(slug=self.slug).exists():
				self.slug = f"c_{name.lower()}_{str(count)}"
				count += 1
			super().save(*args,**kwargs)

	def __str__(self):
		return self.name

	@property
	def get_total_selling(self):
		menu  = self.menu_set.all()
		total = 0
		for i in menu:
			for k in i.orderitem_set.all():
				total += k.quatity
			for k in i.tableorderitem_set.all():
				total += k.quatity
		return total

	class Meta:
		verbose_name_plural = 'Categories'
		ordering = ('name',)



class Menu(models.Model):
	SIZE_CHOICE = (
		('S','Small'),
		('M','Medium'),
		('L','Large')
		) 
	category = models.ManyToManyField(Category)
	name = models.CharField(max_length=100,null=True)
	size = models.CharField(max_length=20,choices= SIZE_CHOICE,blank=True)
	price = models.IntegerField()
	slug = models.SlugField(max_length=50,unique=True,null=True,blank=True)
	image = CloudinaryField('image')

	def save(self,*args,**kwargs):
		if not self.slug:
			name = self.name.split(' ')
			name = ''.join(name)
			self.slug = f"m_{name.lower()}"
			count = 1
			while Menu.objects.filter(slug=self.slug).exists():
				self.slug = f"m_{name.lower()}_{str(count)}"
				count += 1
			super().save(*args,**kwargs)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Menus'
		ordering = ('name',)

	@property
	def get_total_selling(self):
		orderitem  = self.orderitem_set.all()
		tableorder = self.tableorderitem_set.all()
		total = 0
		for i in orderitem:
			total += i.quatity
		for i in tableorder:
			total += i.quatity
		return total



class Order(models.Model):
	STATUS_CHOICE = (
		('Cooking','Cooking'),
		('Delivering','Delivering'),
		('Delivered','Delivered')
		)
	user = models.ForeignKey(MUser, on_delete=models.CASCADE)
	order_date = models.DateField(blank=True,null=True)
	order_time = models.TimeField(blank=True,null=True)
	order_id = models.CharField(max_length=100,null=True,blank=True)
	slug = models.SlugField(max_length=50,null=True,unique=True,editable=True,blank=True)
	ckecked = models.BooleanField(default=False,null=True)
	status 	= models.CharField(max_length=20,choices= STATUS_CHOICE,blank=True,default='Cooking',null=True)


	def save(self,*args,**kwargs):
		
		if not self.order_id:
			counter = 1
			self.order_id = f'O_{counter}'
			while Order.objects.filter(order_id=self.order_id).exists():
				counter += 1
				self.order_id = f'O_{counter}'

		if not self.slug:
			self.slug = self.order_id
		super().save(*args,**kwargs)

	@property
	def get_order_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_sub_total for item in orderitems])
		return total

	@property
	def get_order_qty(self):
		orderitems = self.orderitem_set.all()
		total = sum([x.quatity for x in orderitems])

		return total


	


class OrderItem(models.Model):
	order = models.ForeignKey(Order,on_delete=models.CASCADE)
	item = models.ForeignKey(Menu,on_delete=models.PROTECT)
	quatity = models.IntegerField(default=1)
	cooked = models.BooleanField(default=False,null=True)
	slug = models.SlugField(max_length=50,null=True,unique=True,editable=True,blank=True)

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug = uuid.uuid4()
		super().save(*args,**kwargs)
		
	@property
	def get_sub_total(self):
		return self.item.price * self.quatity




