from django.shortcuts import render
from menu.models import Order,OrderItem
from table.models import TableOrder,TableOrderItem
from django.http import HttpResponse , JsonResponse
import json
def orderView(request):
	


	
	return render(request,'chef/orderView.html')


def getOrders(request):
	total_orders = []

	table_order = TableOrderItem.objects.filter(ordered=True,cooked=False)

	for i in table_order:
		total_orders.append(dict(slug=i.slug,order_by = i.order.user.table_no,order_item = i.item.name , quantity = i.quatity))

	orders = Order.objects.filter(ckecked=True)
	
	for order in orders:
		od = order.orderitem_set.filter(cooked=False)
		
		for i in od:
			
			total_orders.append(dict(slug=i.slug,order_by = i.order.order_id,order_item = i.item.name , quantity = i.quatity))

	

	data = {'data':total_orders}
	return JsonResponse(data)

def cookControl(request):
	data = json.loads(request.body)
	cook_id = data['cook_id']
	action = data['action']
	
	if action == 'cooked':
		if OrderItem.objects.filter(slug=cook_id).exists():
			item = OrderItem.objects.get(slug=cook_id)
			item.cooked = True
			item.save()
		else:
			item = TableOrderItem.objects.get(slug=cook_id)
			item.cooked = True
			item.save()

	elif action == 'cancelcook':
		if OrderItem.objects.filter(slug=cook_id).exists():
			item = OrderItem.objects.get(slug=cook_id)
			item.delete()
		else:
			item = TableOrderItem.objects.get(slug=cook_id)
			item.delete()

	return JsonResponse(data)