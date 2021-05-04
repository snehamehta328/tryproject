from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import *
from .models import Account,Product
from django.contrib import messages
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)

from django.contrib.auth.decorators import login_required
from .forms import *


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
                    account=authenticate(email=email,password=raw_password)
                    login(request,account)
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
            print(is_superuser)
            user=authenticate(email=email,password=password)
            print(email," ",password)
            if user:
                login(request,user)
                return redirect('home/')
        else:
            messages.info(request,'Username or password is incorrect')
    else:
        form=AccountAuthenticationForm()
    context['login_form']=form
    return render(request,'tryapp/login.html',context)

@login_required(login_url='login')
def usercart(request):
    return render(request,'tryapp/usercart.html')

@login_required(login_url='login')
def productdetails(request):
    return render(request,'tryapp/productdetails.html')

@login_required(login_url='login')
def orderhistory(request):
    return render(request,'tryapp/orderhistory.html')

    
@login_required(login_url='login')
def profile(request):
    return render(request,'tryapp/profile.html')

@login_required(login_url='adminlogin')
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

@login_required(login_url='adminlogin')
def viewproduct(request):
    productss=Product.objects.all()
    return render(request,'tryapp/viewproduct.html',{'productss':productss})
    
@login_required(login_url='adminlogin')
def updateproduct(request, id):
    obj = get_object_or_404(Product, id = id)
    form = ProductForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        productss=Product.objects.all()
        return render(request,'tryapp/viewproduct.html',{'productss':productss})
    context={'form':form}
    return render(request, "tryapp/updateproduct.html", context)

@login_required(login_url='adminlogin')
def deleteproduct(request, id):
    context ={}
    obj = get_object_or_404(Product, id = id)
    if request.method =="POST":
        obj.delete()
        productss=Product.objects.all()
        return render(request,'tryapp/viewproduct.html',{'productss':productss})
  
    return render(request, "tryapp/deleteproduct.html", context)

def adminlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        is_superuser=request.POST.get('is_superuser')
        print(is_superuser)
        # print(username," ",password)
        # if email=='admin@gmail.com' and password=='admin123user':
        if is_superuser==1:
            print("successfull")
            user=authenticate(request,email=email,password=password)
            if user is not None:
               login(request,user)
               return redirect('viewproduct/')
            else:
               messages.info(request,'Username or password is incorrect')
        else:
            messages.info(request,'Username or password is incorrect')
    context={}
    return render(request,'tryapp/adminlogin.html',context)

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