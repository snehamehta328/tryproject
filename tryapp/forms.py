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