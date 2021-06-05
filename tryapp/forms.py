from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
# from .models import UserReg
# from .views import signup
from .models import Account,Product




class signupform(forms.ModelForm):
    class Meta:
        model=Account
        fields = "__all__"

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(max_length=100,help_text='Required. Add a valid email address')

    class Meta:
        model=Account
        fields=("email","username","password1","password2","phone_no")



class AccountAuthenticationForm(forms.ModelForm):
    password=forms.CharField(label="Password",widget=forms.PasswordInput)
    class Meta:
        model=Account
        fields=("email","password")
        
    # def save(self):
    #     username=self.cleaned_data['username']
    #     password=self.cleaned_data['password']
    #     user=authenticate(username=username,password=password)
    #     if user:
    #         login(request,user)

    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password=self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid login")

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = "__all__"

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('email','username','phone_no')
    
    def clean_email(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            try:
                account=Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)
    
    def clean_username(self):
        if self.is_valid():
            username=self.cleaned_data['username']
            try:
                account=Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use. Please choose some other username' % username)

    def clean_phoneno(self):
        if self.is_valid():
            phone_no=self.cleaned_data['phone_no']
            try:
                account=Account.objects.exclude(pk=self.instance.pk).get(phone_no=phone_no)
            except Account.DoesNotExist:
                return phone_no
            raise forms.ValidationError('Phone number "%s" is already in use, Please enter a different phone number' % phone_no)

class CheckoutForm(forms.Form):
    # first_name = forms.CharField(max_length=255)
    # last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    place = forms.CharField(max_length=255)
    stripe_token = forms.CharField(max_length=255)
