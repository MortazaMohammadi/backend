from django.contrib import admin
from .models import CustomUser, Employee, Money, Payment_type, Payment, Manager, Boss, Location, Customer, VisaType, Visa, VisaRecivedDoc, visaPayment

admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Money)
admin.site.register(Payment_type)
admin.site.register(Payment)
admin.site.register(Manager)
admin.site.register(Boss)
admin.site.register(Location)
admin.site.register(Customer)
admin.site.register(VisaType)
admin.site.register(Visa)
admin.site.register(VisaRecivedDoc)
admin.site.register(visaPayment)