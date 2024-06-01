from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from .models import * 
from django.db.models import Q
from .utils import *
from .forms import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test

def is_staff(user):
    return user.is_authenticated and user.is_staff

def home(request):
  data = cartData(request)
  user = Customer.objects.all()
  cartItems = data['cartItems']
  order = data['order']
  items = data['items']

  products = Product.objects.all()
  context = {'products':products, 'cartItems':cartItems, "user": user,}
  return render(request, 'store/home.html', context)
  
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
                if user.is_staff:
                    return redirect('menu_admin')
                return redirect('success')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

@login_required
def success(request):
    return render(request, 'store/successfull.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def user_page(request):
    data = cartData(request)
    cartItems = data['cartItems']
    user = Customer.objects.all()
    customer = request.user.customer
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('user_page')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'store/user.html', {'form': form, 'customer': customer, "user": user, 'cartItems': cartItems,})

@login_required
def store(request):
	data = cartData(request)
  
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)
 
@login_required
def menu(request):
    template_name = 'menu/index.html'
    
    user = Customer.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    products = Product.objects.all()
    menu1 = Product.objects.filter(Q(category__iexact='Food'))
    menu2 = Product.objects.filter(Q(category__iexact='Drink'))
    menu3 = Product.objects.filter(Q(category__iexact='Dessert'))
    
    context = { 
        "user": user,
        "menu1": menu1, 
        "menu2": menu2, 
        "menu3": menu3, 
        'products': products, 
        'cartItems': cartItems, 
    }
    
    return render(request, template_name, context)


def tnc(request):
    
    user = Customer.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
      
    context = { 
        "user": user,
        'cartItems': cartItems, 
    }
    template_name = 'menu/tnc.html'
    return render(request, template_name, context)
    
def hns(request):
    user = Customer.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
      
    context = { 
        "user": user,
        'cartItems': cartItems, 
    }
    template_name = 'menu/contact.html'
    return render(request, template_name, context)
  
def aboutus(request):
    user = Customer.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
      
    context = { 
        "user": user,
        'cartItems': cartItems, 
    }
    template_name = 'menu/aboutus.html'
    return render(request, template_name, context)
  
@login_required
def checkout(request):
    data = cartData(request)
    user = Customer.objects.all()
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if order.get_cart_total == 0:
    	return redirect('store')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
    else:
        form = CheckoutForm(user=request.user)

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'form': form, "user": user,}
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
		if orderItem.is_available:
			orderItem.quantity = (orderItem.quantity + 1)
		else:
			return JsonResponse('Produk tidak tersedia', safe=False)
	elif action == 'remove':
		if orderItem.quantity > 0:
			orderItem.quantity = (orderItem.quantity - 1)
		else:
			return JsonResponse('Produk tidak tersedia', safe=False)
	
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

@login_required
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		Transaction.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		)

	return JsonResponse('Payment submitted..', safe=False)
	
@login_required
def orderHistory(request):
    user = Customer.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
      
    orders = Order.objects.filter(customer__user=request.user, complete=True).order_by('-date_ordered')
    order_history = []

    for order in orders:
        items = OrderItem.objects.filter(order=order)
        order_data = {
            'order_id': order.transaction_id,
            'date_ordered': order.date_ordered,
            'total_price': order.get_cart_total,
            'items': items,
             
        }

        order_history.append(order_data)

    context = {'order_history': order_history, "user": user, 'cartItems': cartItems,}
    return render(request, 'store/orderhistory.html', context)

@user_passes_test(is_staff)
def product_list(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')
    else:
        form = ProductForm()

    return render(request, 'store/product_list.html', {'form': form, 'products': products})

@user_passes_test(is_staff)
def menu_admin(request):
    template_name = 'store/menu_admin.html'

    products = Product.objects.all()
    menu1 = Product.objects.filter(Q(category__iexact='Food'))
    menu2 = Product.objects.filter(Q(category__iexact='Drink'))
    menu3 = Product.objects.filter(Q(category__iexact='Dessert'))
    
    context = { 
        "menu1": menu1, 
        "menu2": menu2, 
        "menu3": menu3, 
        'products': products, 
    }
    
    return render(request, template_name, context)
 
@user_passes_test(is_staff)
def product_edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_edit.html', {'form': form, 'product': product})

@user_passes_test(is_staff)
def product_delete(request, pk):
    products = Product.objects.all()
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('menu_admin')