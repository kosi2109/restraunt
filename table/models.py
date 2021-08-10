from django.db import models
from menu.models import Menu,UserNew


class Table(models.Model):
	user = models.OneToOneField(UserNew,on_delete=models.CASCADE,related_name='table')
	table_no = models.CharField(max_length=50,null=True)

	def __str__(self):
		return self.table_no

class TableOrder(models.Model):
	user = models.ForeignKey(Table, on_delete=models.CASCADE)
	order_date = models.DateField(blank=True,null=True)
	order_time = models.TimeField(blank=True,null=True)
	order_id = models.CharField(max_length=100,null=True,blank=True)
	slug = models.SlugField(max_length=50,null=True,unique=True,editable=True,blank=True)
	ckecked = models.BooleanField(default=False,null=True)


	def save(self,*args,**kwargs):
		
		if not self.order_id:
			counter = 1
			self.order_id = f'T_{counter}'
			while TableOrder.objects.filter(order_id=self.order_id).exists():
				counter += 1
				self.order_id = f'T_{counter}'

		if not self.slug:
			self.slug = self.order_id
		super().save(*args,**kwargs)

	@property
	def get_order_total(self):
		orderitems = self.tableorderitem_set.all()
		total_list = []
		
		for item in orderitems:
			if item.ordered == True:
				total_list.append(item.get_sub_total)

		total = sum(total_list)
		return total

	@property
	def get_order_qty(self):
		orderitems = self.tableorderitem_set.all()
		total = sum([x.quatity for x in orderitems])

		return total


	class Meta:
		verbose_name_plural = 'Orders'
		ordering = ('-order_time',)


class TableOrderItem(models.Model):
	order = models.ForeignKey(TableOrder,on_delete=models.CASCADE)
	item = models.ForeignKey(Menu,on_delete=models.PROTECT)
	quatity = models.IntegerField(default=1)
	cooked = models.BooleanField(default=False,null=True)
	ordered = models.BooleanField(default=False,null=True)

	@property
	def get_sub_total(self):
		return self.item.price * self.quatity


