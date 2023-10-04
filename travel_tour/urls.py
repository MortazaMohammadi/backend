from django.urls import path
from django.conf.urls.static import static
from Exellent import settings
from .views import *
urlpatterns =[

    path('', loginPage, name='loginPage'),
     path('logout' , logout_user),
    path('addPayment', addPayment, name='addPayment'),
    path('paymentList', paymentList, name='paymentList'),
    path('paymentUpdate<int:pay_id>/', paymentUpdate, name='paymentUpdate'),
    path('customerRegister',customerRegister, name='customerRegister'),
    path('customerList',customerList, name='customerList'),
    path('visaRegister',visaRegister, name= 'visaRegister'),
    path('visaList',visaList,name='visaList'),
    path('visaView/<int:visa_id>/',visaView,name='visaView'),
    path('visaUpdate/<int:visa_id>/',visaUpdate,name='visaUpdate'),
    path('bill', bill ,name = 'bill'),
    path('billprint/<int:bill_id>/',billPrint,name = 'billPrint'),
    path('deleteBill/<int:bill_id>/',deleteBill,name = 'deleteBill'),
    path('sendBill/<int:bill_id>/',sendBill,name = 'sendBill'),
    path('updateBill/<int:bill_id>/',updateBill,name = 'updateBill'),
    path('customerUpdate/<int:customer_id>/',customerUpdate,name = 'customerUpdate'),
    path('registerPayment/<int:visa_id>/',registerPayment,name = 'customerUpdate')
    
    
    # path('', home_page),

 
]
if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
