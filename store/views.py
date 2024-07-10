from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder


def store(request):

	data = cartData(request)
	cartItems = data['cartItems']


	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
		
	context = {'items':items,'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


from django.views import generic
class ProductListView(generic.ListView):
	model = Product 
	
class ProductDetailView(generic.DetailView):
	model = Product

class OrderListView(generic.ListView):
	model = Order

	
class OrderDetailView(generic.DetailView):
	model = Order	

class OrderItemListView(generic.ListView):
	model = OrderItem
	

class CustomerListView(generic.ListView):
	model = Customer
	
class CustomerDetailView(generic.DetailView):
	model = Customer



def add_product(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		price = request.POST.get('price')
		code = request.POST.get('code')
		group_code = request.POST.get('group_code')
		group_name = request.POST.get('group_name')
		product = Product.objects.create(name=name, price=price, code=code, group_code=group_code, group_name=group_name)
		product.save()
		return redirect('/products/')
	return render(request, 'store/add_product.html')

def add_customer(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		cus_code = request.POST['cus_code']
		segment_code = request.POST['segment_code']
		segment_decription = request.POST['segment_decription']
		customer = Customer.objects.create(name=name, email=email, cus_code=cus_code, segment_code=segment_code, segment_decription=segment_decription)
		customer.save()
		return redirect('/customers/')
	return render(request, 'store/add_customer.html')

def add_order(request):
	if request.method == 'POST':
		customer_id = request.POST['customer']
		date_ordered = request.POST['date_ordered']
		code = request.POST['code']
		transaction_id = request.POST['transaction_id']
		customer = Customer.objects.get(id=customer_id)
		order = Order.objects.create(customer=customer,date_ordered=date_ordered,transaction_id=transaction_id, code=code)
		order.save()
		return redirect('/orders/')
	orders = Order.objects.all()
	customers = Customer.objects.all()
	context={'orders':orders, 'customers':customers}
	return render(request, 'store/add_order.html', context)


