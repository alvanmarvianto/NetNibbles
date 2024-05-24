from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from django.db.models import Q
from .utils import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('success')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

@login_required
def success(request):
    return render(request, 'store/successfull.html')


def promo(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/promo.html', context)

def home(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/home.html', context)

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)
 
   
def menu(request):
  template_name = 'menu/index.html'
  menu1 = Product.objects.filter(Q(category__iexact='Food') |
                              Q(category__icontains='Food'))
  menu2 = Product.objects.filter(Q(category__iexact='Drink') |
                              Q(category__icontains='Drink'))
  menu3 = Product.objects.filter(Q(category__iexact='Dessert') |
                              Q(category__icontains='Dessert'))
    
  context = { "menu1": menu1, "menu2": menu2, "menu3": menu3 }
  return render(request, template_name, context)

def tnc(request):
    template_name = 'menu/tnc.html'
    return render(request, template_name)
    
def hns(request):
    template_name = 'menu/contact.html'
    return render(request, template_name)

def aboutus(request):
    template_name = 'menu/aboutus.html'
    return render(request, template_name)


@login_required
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
    else:
        form = CheckoutForm(user=request.user)

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'form': form}
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

def orderHistory(request):
    orders = Order.objects.filter(customer__user=request.user).order_by('-date_ordered')
    order_history = []

    for order in orders:
        items = OrderItem.objects.filter(order=order)
        order_data = {
            'order_id': order.id,
            'date_ordered': order.date_ordered,
            'total_price': order.get_cart_total,
            'items': items,
        }
        order_history.append(order_data)

    context = {'order_history': order_history}
    return render(request, 'store/orderhistory.html', context)