from django.urls import path
from . import views


urlpatterns=[
    path('main/',views.main,name='main'),
    path('home/',views.home,name='home'),
    path('login/',views.loginview,name='login'),
    path('signup/',views.signup,name='signup'),
    path('productd/',views.productdetails,name='productd'),
    path('orderh/',views.orderhistory,name='orderh'),
    path('profile/',views.profile,name='profile'),
    path('cart/',views.usercart,name='cart'),
    path('signup/login/',views.loginview,name='login'),
    path('login/home/',views.home,name='home'),
    path('signup/home/',views.home,name='home'),
    path('signup/login/home/',views.home,name='home'),
    path('logout/', views.logout_view, name="logout"),
    path('logout/main/',views.main,name="main"),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminlogin/viewproduct/addproduct/',views.addproductform,name='addproduct'),
    path('adminlogin/viewproduct/',views.viewproduct,name='view'),
    path('adminlogin/viewproduct/addproduct/viewproduct/',views.viewproduct),
    path('update/<id>',views.updateproduct,name='update'),
    path('delete/<id>',views.deleteproduct,name='delete'),
    path('cloth/',views.clothes,name='cloth'),
    path('electronics/',views.electronics,name='elec'),
    path('book/',views.books,name='book'),
    path('shoes/',views.shoes,name='shoes'),
    # path('adminlogin/',views.adminlogin,name='adminlogin'),
    # path('adminlogin/addproduct/',views.addproductform,name='adproduct'),
    # path('adminlogin/addproduct/success/',views.successfull,name='success'),
]
