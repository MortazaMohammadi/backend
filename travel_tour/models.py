from django.db import models
from django.contrib.auth.models import AbstractUser

# user Model
class CustomUser(AbstractUser):
    users_type = (
        ('Employee','Employee'),
        ('Manager','Manager'),
        ('Boss','Boss')
    )
    user_type = models.CharField(choices=users_type , max_length=50,default='Agent')
    profile_image = models.ImageField(upload_to='profiles/' , blank= True, null=True)

    def __str__(self):
        return   str(self.first_name) + ' ' + str(self.last_name)
    
    
# employee
class Employee(models.Model):
    admin = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=50)
    def __str__ (self):
        return str(self.admin)
    
# money
class Money(models.Model):
    money_type = models.CharField(max_length=5)
    amount = models.IntegerField()
    sell_amount = models.FloatField()
    buy_amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    
# Payment type
class Payment_type(models.Model):
    title = models.CharField(max_length=20)


# Payment
class Payment(models.Model):
    amount = models.FloatField(max_length=10)
    money = models.ForeignKey(Money, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(Payment_type, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    


# Manager
class Manager (models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    registration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=50)
    
    def __str__ (self):
        return str(self.admin)

# Boss
class Boss (models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    registeration_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=50)
    def __str__(self) -> str:
        return str(self.admin)
    
class Location (models.Model):
    city = models.CharField(max_length=20)
class Customer(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    mainstate = models.CharField(max_length=20)
    currentstate = models.CharField(max_length=20)
    passport = models.IntegerField(null=True)
    profile = models.ImageField(upload_to='profile/' , blank= True, null=True)
    passportImage = models.ImageField(upload_to='document/' , blank= True, null=True)
    cardImage = models.ImageField(upload_to='document/' , blank= True, null=True)
    
class VisaType(models.Model):
    country = models.CharField(max_length=20)
    duration = models.IntegerField()
    type = models.CharField(max_length=20)
    price = models.FloatField()
class Visa(models.Model):
    visaType = models.ForeignKey(VisaType, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    isprocess = models.BooleanField(default=False)
    isapproved = models.BooleanField(default=False)
    ispayed = models.BooleanField(default=False)
    isdone = models.BooleanField(default=False)
    
class VisaRecivedDoc(models.Model):
    visa = models.ForeignKey(Visa, on_delete=models.CASCADE)
    Document = models.CharField(max_length=60, null = True)
class visaPayment(models.Model):
    visa = models.ForeignKey(Visa,on_delete=models.CASCADE)
    payed = models.FloatField(null = True)
    Blockaddress = models.CharField(max_length=50, null = False)
    Blockimage = models.ImageField(upload_to='document/' , blank= True, null=True)
    
# Create your models here.
