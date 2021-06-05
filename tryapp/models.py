from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import pre_save,post_save
# from django.dispatch import receiver
import datetime
class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username")
        user=self.model(
            email=self.normalize_email(email), 
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,password):
        user=self.create_user(
            email=self.normalize_email(email),
             username=username,
             password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email=models.EmailField(verbose_name="email",max_length=100,unique=True)
    username=models.CharField(max_length=30,unique=True)
    phone_no=models.CharField(max_length=10,unique=True)
    date_joined=models.DateTimeField(verbose_name="date joined" , auto_now_add=True)
    last_login=models.DateTimeField(verbose_name="last joined" , auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    # hide_email=models.BooleanField(default=True)

    objects=MyAccountManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

    class Meta:
         db_table="signuptable"


CATEGORIES=[
    ("CLOTHES","Clothes"),
    ("ELECTRONICS","Electronics"),
    ("BOOKS","Books"),
    ("SHOES","Shoes")
]

class Product(models.Model):
    category=models.CharField(max_length=200,choices=CATEGORIES)
    productname = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.CharField(max_length=5000, null=True, blank=True)

    class Meta:
        db_table="pro"

    # @staticmethod
    # def get_products_by_id(id):
    #     return Product.objects.filter(id__in =id)


# class Order(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     customer = models.ForeignKey(Account,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.IntegerField()
#     address = models.CharField(max_length=50, default='', blank=True)
#     phone = models.CharField(max_length=50, default='', blank=True)
#     date = models.DateField(default=datetime.datetime.today)
#     status = models.BooleanField(default=False)

#     def placeOrder(self):
#         self.save()
    
#     @staticmethod
#     def get_orders_by_customer(customer_id):
#         return Order.objects.filter(customer=customer_id).order_by('-date')   
# 
# class Cart(models.Model):
#     user =models.ForeignKey(Account,on_delete = models.CASCADE)
#     # product = models.ForeignKey(Product,on_delete = models.CASCADE)
#     # product_id = models.CharField(max_length=100)
#     quantity = models.IntegerField()
#     # status = models.BooleanField(default=False)
#     # added_on =models.DateTimeField(auto_now_add=True,null=True)
#     # update_on = models.DateTimeField(auto_now=True,null=True)

#     def __str__(self):
#         return self.user.username


