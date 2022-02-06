from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomerRegistrationForm, LoginForm, MyPasswordChangeForm, CustomerProfileForm
from .models import Customer, Product, Cart, OrderPlaced
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


class ProductView(View):
    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')

        return render(request, 'app/home.html', {'mobiles': mobiles,
        'laptops':laptops})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user, product=product).save()
    return redirect('show-cart')

def showCart(request):
    user = request.user
    if user.is_authenticated:
        cart_items = Cart.objects.filter(user = user)
        amount = 0.0
        shipping_charge = 40
        total_amount = 0.0
        cart_item_list = [cart_item for cart_item in cart_items]
        # print(type(cart_item_list[0].product.discounted_price))

        if cart_item_list:
            for p in cart_item_list:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
                total_amount = amount + shipping_charge
   
        return render(request, 'app/addtocart.html', {
            'cart_items':cart_items, 'total_amount':total_amount,'amount':amount
       })


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_charge = 40
        total_amount = 0.0
        cart_item_list = [cart_item for cart_item in Cart.objects.all() if cart_item.user == request.user]
        for p in cart_item_list:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
            total_amount = amount + shipping_charge

            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':total_amount


            }
   
    return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_charge = 40
        total_amount = 0.0
        cart_item_list = [cart_item for cart_item in Cart.objects.filter(user = request.user)]
        for p in cart_item_list:

            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
            total_amount = amount + shipping_charge

            data = {
                'quantity':c.quantity,
                'amount':amount,
                'totalamount':total_amount
            }
    return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        amount = 0.0
        shipping_charge = 40
        cart_item_list = [cart_item for cart_item in Cart.objects.all() if cart_item.user ==request.user]
        for p in cart_item_list:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
             'amount':amount,
            'totalamount':amount + shipping_charge
            }
        return JsonResponse(data)
    else:
       return HttpResponse("ritik")


def buy_now(request):
    return render(request, 'app/buynow.html')


def address(request):
    customerDetails = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', {
        'active': 'btn-primary',
        'customerDetails':customerDetails
    })


def orders(request):
    return render(request, 'app/orders.html')


def mobile(request, brand=None):
    if brand == None:
        mobiles = Product.objects.filter(category='M')
    elif brand == 'samsung' or brand == 'mi' or brand == 'redmi' or brand == 'apple':
        mobiles = Product.objects.filter(category='M', brand=brand)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


# def login(request):
#  return render(request, 'app/login.html')


class customerregistration(View):
    # if request method is get then
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    # if request method is post

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


def checkout(request):
    return render(request, 'app/checkout.html')


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        
        return render(request, 'app/profile.html', {
            'form': form,
            'active': 'btn-primary',
        })

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user = usr,name=name,
                           locality=locality,
                           city=city,
                           state=state,
                           zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfull')
        return render(request, 'app/profile.html',{'form':form,
        'active':'btn-primary'})