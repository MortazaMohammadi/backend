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
    money_type = models.CharField(max_length=20)
    amount = models.IntegerField()
    sell_amount = models.FloatField()
    buy_amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return str(self.money_type)
# Payment type
class Payment_type(models.Model):
    title = models.CharField(max_length=20)
    def __str__ (self):
        return str(self.title)


# Payment
class Payment(models.Model):
    amount = models.FloatField(max_length=10)
    money = models.ForeignKey(Money, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(Payment_type, on_delete=models.CASCADE)
    date = models.DateField()
    


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
    email = models.CharField(max_length=50,default='unknown')
    phone = models.CharField(max_length=50)
    mainstate = models.CharField(max_length=20)
    currentstate = models.CharField(max_length=20)
    passport = models.CharField(max_length=50,null=True)
    profile = models.ImageField(upload_to='profile/' , blank= True)
    passportImage = models.ImageField(upload_to='document/' , blank= True, null=True)
    cardImage = models.ImageField(upload_to='document/' , blank= True, null=True)
    def __str__ (self):
        return str(self.name)+ ' ' + str(self.lastname)

class OurEmail(models.Model):
     email = models.CharField(max_length=60)
     def __str__ (self):
        return str(self.email)


class VisaType(models.Model):
    country = models.CharField(max_length=20)
    duration = models.IntegerField()
    type = models.CharField(max_length=20)
    price = models.FloatField()
    money = models.ForeignKey(Money, on_delete=models.CASCADE)
    def __str__ (self):
        return str(self.country)+ ' ' + str(self.duration)

class otherbill(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    def __str__(self):
        return str(self.title)
    
class Bill(models.Model):
    name = models.CharField(max_length=50)
    reciveddoc = models.CharField(max_length=50)
    visatype = models.ForeignKey(VisaType, on_delete=models.CASCADE,null=True)
    othertype = models.ForeignKey(otherbill,on_delete=models.CASCADE,null=True)
    date = models.DateField(auto_now_add = True)
    price = models.FloatField()
    payed = models.FloatField()
    money = models.ForeignKey(Money, on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    isdone = models.BooleanField(default=False)
    cr = models.BooleanField(default=False)
    cv = models.BooleanField(default=False)
    mainprice = models.FloatField(default=0)
    peopleNo = models.IntegerField(default = 1)
    phone = models.CharField(default='07....', max_length=15)
    isactive = models.BooleanField(default=True)
    isprint = models.BooleanField(default = False)
    def __str__(self):
        return str(self.name) + str(self.peopleNo)

class Visa(models.Model):
    visaType = models.ForeignKey(VisaType, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    isprocess = models.BooleanField(default=False)
    employee = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    emailby = models.ForeignKey(OurEmail, on_delete=models.CASCADE)
    visapdf = models.FileField(upload_to='VisaPdfFiles/', null= True)
    Otherdocs = models.FileField(upload_to='VisaPdfFiles/', null= True, default=None)
    isapproved = models.BooleanField(default=False)
    isrejected = models.BooleanField(default=False)
    iscomplate = models.BooleanField(default=False)
    saveddate = models.DateField(auto_now_add = True)
    price = models.FloatField()
    money = models.ForeignKey(Money, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill,on_delete=models.CASCADE,null=True)


class registerPayed(models.Model):
    visa = models.ForeignKey(Visa ,null=True, on_delete=models.SET_NULL)
    payed = models.FloatField(null=True)
    money = models.ForeignKey(Money, null=True, on_delete=models.CASCADE)
    
    
class VisaRecivedDoc(models.Model):
    visa = models.ForeignKey(Visa, on_delete=models.CASCADE)
    Document = models.CharField(max_length=60, null = True)
    def __str__ (self):
        return str(self.Document)
class visaPayment(models.Model):
    visa = models.ForeignKey(Visa,on_delete=models.CASCADE)
    payed = models.FloatField(null = True)
    blockAddress = models.CharField(max_length=50, null = True)
    blockImage = models.ImageField(upload_to='BlockImage/' , blank= True, null=True)
    def __str__ (self):
        return str(self.payed)+ ' ' + str(self.blockAddress)
    
#  points
class Notes(models.Model):
    notetype = (
        ('پرداخت','پرداخت'),
        ('دریافت','دریافت')
    )
    name = models.CharField(max_length=50)
    whatfor = models.CharField(max_length=100)
    type = models.CharField(choices=notetype , max_length=50,default='pay')
    amount =models.FloatField()
    money = models.ForeignKey(Money,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
# Create your models here.
class BCV(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null= True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null= True)
    visa = models.ForeignKey(Visa, on_delete=models.CASCADE, null= True) 

class qararrtype(models.Model):
    title = models.CharField(max_length=50)    
class qararrdad(models.Model):
    name = models.CharField(max_length=50)
    fname = models.CharField(max_length=20)
    passport = models.CharField(max_length=20)
    price = models.FloatField(default='0')
    phone = models.CharField(max_length=12)
    date = models.DateField(auto_now_add=True)
    payed = models.FloatField(default=0)
    type = models.ForeignKey(qararrtype, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    done = models.BooleanField(default=False)
    def __str__(self) -> str:
        return str(self.name)
