from django.contrib import admin
from .models import BCV, Bill, CustomUser, Employee, Money, OurEmail, Payment_type, Payment, Manager, Boss, Location, Customer, VisaType, Visa, VisaRecivedDoc, qararrdad, qararrtype, registerPayed, visaPayment,Notes,otherbill

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
admin.site.register(OurEmail)
admin.site.register(registerPayed)
admin.site.register(Notes)
admin.site.register(Bill)
admin.site.register(otherbill)
admin.site.register(BCV)
admin.site.register(qararrdad)
admin.site.register(qararrtype)
