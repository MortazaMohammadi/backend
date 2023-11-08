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
    path('customerRegister/<int:bill_id>/<str:passport_id>/',customerRegister, name='customerRegister'),
    path('customerList',customerList, name='customerList'),
    path('visaRegister/<int:bcv_id>',visaRegister, name= 'visaRegister'),
    path('visaList',visaList,name='visaList'),
    path('visaView/<int:visa_id>/',visaView,name='visaView'),
    path('visaUpdate/<int:visa_id>/',visaUpdate,name='visaUpdate'),
    path('bill', bill ,name = 'bill'),
    path('billprint/<int:bill_id>/',billPrint,name = 'billPrint'),
    path('deleteBill/<int:bill_id>/',deleteBill,name = 'deleteBill'),
    path('sendBill/<int:bill_id>/',sendBill,name = 'sendBill'),
    path('updateBill/<int:bill_id>/',updateBill,name = 'updateBill'),
    
    path('registerPayment/<int:visa_id>/',registerPayment,name = 'registerPayment'),
    path('visaStatistic', visaStatistic,name = 'visaStatistic'),
    path('employeeRegister', employeeRegister, name = 'employeeRegister'),
    path('employeeUpdate/<int:user_id>/', employeeUpdate, name = 'employeeUpdate'),
    path('notes',notes,name = 'notes'),
    path('monayUpdate/', moneyUpdate, name='moneyUpdate'),
    path('billCustomer/',billCustomer,name = 'billCustomer'),
    path('billVisa/', billVisa, name='billVisa'),
    path('crTrue/<int:bill_id>/<str:passport_id>/', crTrue, name='crTrue'),
    path('cvTrue/<int:bill_id>/', cvTrue, name='cvTrue'),
    path('saveBill/<int:bill_id>/',saveBill,name='saveBill'),
    path("billListing", billListing, name="billListing"),
    path('totalstatistics', totalstatistics, name = 'totalstatistics')

    # path('', home_page),

 
]
if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
