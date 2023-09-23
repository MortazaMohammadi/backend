from django.shortcuts import render

# login Page
def loginPage(request):
    context = {'page' : 'صفحه ورود'}
    return render(request, 'acount/loginPage.html',)


# employee registeration page
def employeeRegister(request):
    context = {'page' : 'صفحه راجستر'}
    return render(request, 'acount/employeeRegisteration.html',context)


# add payments
def addPayment(request):
    context = {'page' : 'اضافه مصرف'}
    return render(request, 'office/addPayment',context)


# payment list and static for payment
def paymentList(request):
    context = {'page' : 'لیست مصارف'}
    return render(request, 'office/paymentList',)


# payment update
def paymentUpdate(request, pay_id):
    context = {'page' : 'تغیر مصرف'}
    return render(request, 'office/paymentUpdate',)


# customer registeration page
def customerRegister(request):
    context = {'page' : 'راجستر مشتری'}
    return render(request, 'customer/customerRegister.html',)



# customer list
def customerList(request):
    context= {'page': 'لیست مشتریان'}
    return render(request, 'customer/customerList.html', context)



# visa registeration page
def visaRegister(request):
    context = {'page' : 'راجستر ویزا'}
    return render(request, 'visa/visaRegister.html',)


# visa list update cancel save payed approved search engine
def visaList(request):
    context = {'page' : 'لیست ویزا'}
    return render(request, 'visa/visaList.html',)


# visa View 
def visaView(request, visa_id):
    context = {'page' : 'مشخصات ویزا'}
    return render(request, 'visa/visaView.html',)


# visa update 
def visaUpdate(request,visa_id):
    context = {'page' : 'اپدیت ویزا'}
    return render(request, 'visa/visaUpdate.html',context)

