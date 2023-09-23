from django.urls import path
from .views import *
urlpatterns =[

    path('',loginPage),
    path('employeeRegister', employeeRegister, name='employeeRegisteration'),
    path('addPayment', addPayment, name='addPayment'),
    path('paymentList', paymentList, name='paymentList'),
    path('paymentUpdate<int:pay_id>/', paymentUpdate, name='paymentUpdate'),
    path('customerRegister',customerRegister, name='customerRegister'),
    path('customerList',customerList, name='customerList'),
    path('visaRegister',visaRegister, name= 'visaRegister'),
    path('visaList',visaList,name='visaList'),
    path('visaView/<int:visa_id>/',visaView,name='visaView'),
    path('visaUpdate',visaUpdate,name='visaUpdate'),
    
    # path('', home_page),

 
]