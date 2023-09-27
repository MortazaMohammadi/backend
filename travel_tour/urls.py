from django.urls import path
from django.conf.urls.static import static
from Exellent import settings
from .views import *
urlpatterns =[

    path('', loginPage, name='loginPage'),
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
if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
