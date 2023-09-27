from django.shortcuts import render
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth import login, logout , authenticate , update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import Http404 , HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from travel_tour.EmailBackEnd import EmailBackEnd
from travel_tour import models as mod
from django.db.models import Sum

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
    context = {}
    if request.method == 'POST':
        paymodel = mod.Payment()
        paymodel.amount= request.POST.get('amount_txt')
        money = request.POST.get('mtype_txt')
        paymodel.money = mod.Money.objects.get(id = money)
        paytype = request.POST.get('ptype_txt')
        paymodel.payment_type = mod.Payment_type.objects.get(id = paytype)
        paymodel.date = request.POST.get('date_txt')
        paymodel.save()
        return redirect('/addPayment')
    else:
        context['mtype'] = mod.Money.objects.all()
        context['ptype'] = mod.Payment_type.objects.all()
        context['page'] = 'اضافه مصرف'
        context['list'] = mod.Payment.objects.all()
        return render(request, 'office/addPayment.html',context)


# payment list and static for payment
def paymentList(request):
    context = {}
    if request.method == 'GET':
         Fptype = request.GET.get('ptype_txt')
         if Fptype:
           if Fptype == '0':
               context['records'] = mod.Payment.objects.all()
           else:
                 ptype = mod.Payment_type.objects.get(id=Fptype)  # Use get() instead of filter()
                 context['records'] = mod.Payment.objects.filter(payment_type=ptype.id)
         else:
              context['records'] = mod.Payment.objects.all()
              
              
    total_amount = mod.Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount']
    if total_amount:
        paytype = mod.Payment_type.objects.all()
        context['total_amount'] = total_amount
        if paytype:
            l1 = []
            
            for i in paytype: 
                l2 = []
                i.title
                filtered_amount = mod.Payment.objects.filter(payment_type__id=i.id).aggregate(filtered_amount=Sum('amount'))['filtered_amount']
                l2.append(i.title)
                l2.append(filtered_amount)
                l2.append(round(filtered_amount*100/total_amount,2))
                l1.append(l2)
            context['eachptype'] = l1
            context['paytype'] = mod.Payment_type.objects.all()
    context['page'] = 'لیست مصارف'
    return render(request, 'office/paymentList.html',context)


# customer registeration page
from .models import Customer

def customerRegister(request):
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        lastname = request.POST.get('lastname_txt')
        employee_id = request.POST.get('employee_txt')
        email = request.POST.get('email_txt')
        phone = request.POST.get('phone_txt')
        address = request.POST.get('address_txt')
        mainstate = request.POST.get('mainstate_txt')
        currentstate = request.POST.get('currentstate_txt')
        passport = request.POST.get('passport_txt')
        profile_image = request.FILES.get('profile_imag')
        card_image = request.FILES.get('card_img')
        passport_image = request.FILES.get('passport_img')

        employee = mod.Employee.objects.get(id=employee_id)  # Fetch the employee object using the provided ID

        customer = Customer(
            name=name,
            lastname=lastname,
            employee=employee,
            email=email,
            phone=phone,
            address=address,
            mainstate=mainstate,
            currentstate=currentstate,
            passport=passport,
            profile=profile_image,
            cardImage=card_image,
            passportImage=passport_image
        )
        customer.save()  # Save the customer object to the database

        return redirect('success')  # Redirect to a success page

    employees = mod.Employee.objects.all()  # Fetch all employees to populate the employee field in the form

    return render(request, 'visa/customerRegister.html', {'employees': employees,'page': 'راجستر مشتری'})


# payment update
def paymentUpdate(request, pay_id):
    context = {'page' : 'آمار مصرف'}
    return render(request, 'office/paymentUpdate', context)


# customer list
def customerList(request):
    context= {'page': 'لیست مشتریان'}
    return render(request, 'visa/customerList.html', context)



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

# Login user_account view
def loginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        user = EmailBackEnd.authenticate(
            request, username=user_name, password=password)
        if user != None:
            login(request, user)
            return redirect('/my_listing_dashboard_view')
        else:
            context['aut']= 'نام کاربری یا رمز عبور تان اشتباه است.'
    return render(request, 'account/login.html',context)
# End of user_account view