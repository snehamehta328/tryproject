from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import *
from .models import Account,Product
from django.contrib import messages
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import *
import stripe 

from django.conf import settings
from django.contrib import messages
# from django.shortcuts import render, redirect

from .cart import Cart
# from .forms import CheckoutForm


# Create your views here.
def main(request):
    return render(request,'tryapp/frontpage.html')



def signup(request):
    context={}
    if request.user.is_authenticated:
        return redirect('home/')
    else:
        if request.method=='POST':
            if request.POST.get('username') and request.POST.get('email') and request.POST.get('password1'):
                form=RegistrationForm(request.POST)
                if form.is_valid():
                    form.save()
                    email=form.cleaned_data.get('email')
                    raw_password=form.cleaned_data.get('password1')
                    # username=form.cleaned_data.get('username')
                    account=authenticate(email=email,password=raw_password)
                    login(request,account)
                    # messages.success(request,'Account was created for '+username)
                    return redirect('login/')
                else:
                    context['registration_form']=form
        else:
            form=RegistrationForm()
            context['registration_form']=form
        return render(request,'tryapp/signup.html',context)
       

@login_required(login_url='login')
def home(request):
    return render(request,'tryapp/homepage.html')



def logout_view(request):
    logout(request)
    return redirect('main/')

def loginview(request,*args,**kwargs):
    context={}
    user=request.user
    if user.is_authenticated:
        return redirect('home/')


    if request.POST:
        form=AccountAuthenticationForm(request.POST)
        if form.is_valid():
            
            email=request.POST['email']
            password=request.POST['password']
            is_superuser=request.POST.get('is_superuser')
            user=authenticate(email=email,password=password,is_superuser=is_superuser)
            print(email," ",password)
            if user:
                if user.is_superuser==True:
                    login(request,user)
                    return redirect('viewproduct/')
                else:
                   login(request,user)
                   return redirect('home/')
        else:
            messages.info(request,'Username or password is incorrect')
    else:
        form=AccountAuthenticationForm()
    context['login_form']=form
    return render(request,'tryapp/login.html',context)




@login_required(login_url='login')
def productdetails(request):
    return render(request,'tryapp/productdetails.html')

@login_required(login_url='login')
def orderhistory(request):
    return render(request,'tryapp/orderhistory.html')

@login_required(login_url='login')
def shipping(request):
    return render(request,'tryapp/shippingpage.html')


@login_required(login_url='login')
def addproductform(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewproduct/')
    else:
        form=ProductForm()
        context={'form':form}
        return render(request,'tryapp/productadd.html',context)

@login_required(login_url='login')
def viewproduct(request):
    productss=Product.objects.all()
    return render(request,'tryapp/viewproduct.html',{'productss':productss})
    
@login_required(login_url='login')
def updateproduct(request, id):
    obj = get_object_or_404(Product, id = id)
    form = ProductForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        productss=Product.objects.all()
        return render(request,'tryapp/viewproduct.html',{'productss':productss})
    context={'form':form}
    return render(request, "tryapp/updateproduct.html", context)

@login_required(login_url='login')
def deleteproduct(request, id):
    context ={}
    obj = get_object_or_404(Product, id = id)
    if request.method =="POST":
        obj.delete()
        productss=Product.objects.all()
        return render(request,'tryapp/viewproduct.html',{'productss':productss})
  
    return render(request, "tryapp/deleteproduct.html", context)

@login_required(login_url='login')
def updateprofile_view(request):
    if not request.user.is_authenticated:
        return redirect("login/")
    context={}

    if request.POST:
        form=UpdateProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile is updated successfully!')
    else:
        form=UpdateProfileForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "phone_no": request.user.phone_no,
            }
        )
    context['account_form']=form
    return render(request,'tryapp/profile.html',context)
    
def products(request):
    productss=Product.objects.all()
    return render(request,'tryapp/homepage.html',{'productss':productss})

def clothes(request):
    productss=Product.objects.filter(category='CLOTHES')
    return render(request,'tryapp/homepage.html',{'productss':productss})

def electronics(request):
    productss=Product.objects.filter(category='ELECTRONICS')
    return render(request,'tryapp/homepage.html',{'productss':productss})

def books(request):
    productss=Product.objects.filter(category='BOOKS')
    return render(request,'tryapp/homepage.html',{'productss':productss})

def shoes(request):
    productss=Product.objects.filter(category='SHOES')
    return render(request,'tryapp/homepage.html',{'productss':productss})

@login_required(login_url='login')
def viewdesc(request,id):
    product=Product.objects.get(pk=id)
    print(product)
    return render(request,'tryapp/productdetails.html',{'product':product})

@login_required(login_url='login')
def contact(request):
    return render(request, 'tryapp/contact.html')

@login_required(login_url='login')
def viewuser(request):
    userss = Account.objects.all()
    return render(request, 'tryapp/viewuser.html', {'userss': userss})
    
# @login_required(login_url='login')
# def usercart(request):
#     return render(request,'tryapp/usercart.html')


# from apps.order.utilities import checkout, notify_customer, notify_vendor

def usercart(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            try:
                charge = stripe.Charge.create(
                    amount=int(cart.get_total_cost() * 100),
                    currency='USD',
                    description='Charge from Interiorshop',
                    source=stripe_token
                )

                # first_name = form.cleaned_data['first_name']
                # last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']

                # order = checkout(request, email, address, zipcode, place, phone, cart.get_total_cost())

                cart.clear()

                # notify_customer(order)
                # notify_vendor(order)

                return redirect('success')
            except Exception:
                messages.error(request, 'There was something wrong with the payment')
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'tryapp/usercart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

# def success(request):
#     return render(request, 'cart/success.html')

