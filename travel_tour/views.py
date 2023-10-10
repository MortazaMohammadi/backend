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
            return redirect('/addPayment')
        else:
            context['aut']= 'نام کاربری یا رمز عبور تان اشتباه است.'
    return render(request, 'account/login.html',context)


# logout
def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
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
        context['addpay'] = ' text-warning sub-bg '
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
              context['records'] = mod.Payment.objects.order_by('-id') 
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
    context['listpay'] = ' text-warning sub-bg '
    return render(request, 'office/paymentList.html',context)

# Customer Registeration
def customerRegister(request):
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        lastname = request.POST.get('lastname_txt')
        email = request.POST.get('email_txt')
        phone = request.POST.get('phone_txt')
        address = request.POST.get('address_txt')
        mainstate = request.POST.get('mainstate_txt')
        currentstate = request.POST.get('currentstate_txt')
        passport = request.POST.get('passport_txt')
        profile_image = request.FILES['profile_img']
        card_image = request.FILES['card_img']
        passport_image = request.FILES['passport_img']
         # Fetch the employee object using the provided ID

        customer = mod.Customer(
            name=name,
            lastname=lastname,
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

        return redirect('/customerRegister')  # Redirect to a success page



    return render(request, 'visa/customerRegister.html', {'page': 'راجستر مشتری','cusregister':' text-warning sub-bg '})


# visa registeration page
def visaRegister(request):
    context = {}
    if request.method == 'POST':
        visaType = request.POST.get('visaType_txt')
        customer = request.POST.get('customer_txt')
        employee_id = request.POST.get('employee_txt')
        recivedDoc = request.POST.get('recivedDoc_txt')  # Assuming you have a file input field with name 'recived_doc'
        blockAddress = request.POST.get('blockAddress_txt')
        blockImage = request.FILES.get('block_img')  # Assuming you have a file input field with name 'block_image'
        payed = request.POST.get('payed_txt')
        emailBy = request.POST.get('emailBy_txt')
        price = request.POST.get('price_txt')
        money = request.POST.get('money_txt')
        customer = request.POST.get('customer_txt')
        dbcustomer = mod.Customer.objects.get(id= customer)
        dbvisatype = mod.VisaType.objects.get(id= visaType)
        dbemailBy = mod.OurEmail.objects.get(id = emailBy)
        dbmoney = mod.Money.objects.get(id = money)
        employee = mod.Employee.objects.get(id=employee_id) 
        visa = mod.Visa(
            visaType = dbvisatype,
            customer = dbcustomer,
            employee = employee,
            emailby = dbemailBy,
            money = dbmoney,
            price = price
        )
        reciveddoc = mod.VisaRecivedDoc(
            visa = visa,
            Document = recivedDoc,
        )
        visaPayment = mod.visaPayment(
            visa = visa,
            payed = payed,
            blockAddress = blockAddress,
            blockImage = blockImage
        )
        visa.save()
        reciveddoc.save()
        visaPayment.save()
        return redirect('/visaRegister')   
    employees = mod.Employee.objects.all()    
    context['employees'] = employees  
    context['money'] = mod.Money.objects.all()
    context['emailby'] = mod.OurEmail.objects.all()
    context['customers'] = mod.Customer.objects.all().reverse()
    context['visatype'] = mod.VisaType.objects.all()
    context['page'] = 'راجستر ویزا'
    context['visaregister'] = ' text-warning sub-bg '
    return render(request, 'visa/visaRegister.html',context)

# visa list
def visaList(request):
    context = {}
    if request.method == 'GET':
        passport_txt = request.GET.get('passport_txt')
        
        if passport_txt:
            try:
                customer = mod.Customer.objects.get(passport=passport_txt)
                context['visalisting'] = mod.Visa.objects.filter(customer=customer)
            except mod.Customer.DoesNotExist:
                pass
            
            return render(request, 'visa/visaList.html', context)
    
    context['visalisting'] = mod.Visa.objects.all()
    context['visaList'] = 'text-warning sub-bg'
    context['page'] = 'لیست ویزا'
    return render(request, 'visa/visaList.html', context)

# bill print
def bill(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        reciveddoc = request.POST.get('reciveddoc_txt')
        visatype = request.POST.get('visatype_txt')
        price = request.POST.get('price_txt')
        payed = request.POST.get('payed_txt')
        money = request.POST.get('money_txt')
        duration = request.POST.get('duration_txt')
        dbvisatype = mod.VisaType.objects.get(id= visatype)
        dbmoney = mod.Money.objects.get(id = money)
        billing = mod.Bill(
            name = name,
            reciveddoc = reciveddoc,
            visatype = dbvisatype,
            price = price,
            payed = payed,
            money = dbmoney,
            duration = duration
        )
        billing.save()
        return redirect('/bill#list')
    else:
        pass
    context['bill'] = 'text-warning sub-bg'
    context['page'] = 'راجستر بل'
    context['billListing'] = mod.Bill.objects.filter(isdone = False)
    context['visaList'] = mod.VisaType.objects.all()
    context['money'] = mod.Money.objects.all()
    return render(request, 'billing/bill.html', context)

# bill print
def billPrint(request, bill_id):
    context = {}
    bill = mod.Bill.objects.get(id = bill_id)
    
    context['remain']=bill.price - bill.payed
    context['bill'] = bill
    
    return render(request, 'billing/billprint.html',context)

# bill delete
def deleteBill(request, bill_id):
    mod.Bill.objects.get(id = bill_id).delete()
    return redirect('/bill#list')

# bill send for register
def sendBill(request, bill_id):
    mod.Bill.objects.get(id = bill_id).isdone = True
    return redirect('/bill#list')

# bill update
def updateBill(request, bill_id):
    bill = mod.Bill.objects.get(id = bill_id)
    context={}
    if request.method == 'POST':
        bill.name = request.POST.get('name_txt')
        bill.reciveddoc = request.POST.get('reciveddoc_txt')
        visatype = request.POST.get('visatype_txt')
        bill.price = request.POST.get('price_txt')
        bill.payed = request.POST.get('payed_txt')
        money = request.POST.get('money_txt')
        bill.visatype = mod.VisaType.objects.get(id= visatype)
        bill.money = mod.Money.objects.get(id = money)
        bill.duration = request.POST.get('duration_txt')
        bill.save()
        return redirect('/bill#list')
    else:
        context['bill'] = bill
        context['visaList'] = mod.VisaType.objects.all()
        context['money'] = mod.Money.objects.all()
    return render(request, 'billing/updateBill.html', context)
    
# visa View 
def visaView(request, visa_id):
    visa = mod.Visa.objects.get(id=visa_id)
    visapayment = mod.visaPayment.objects.get(visa=visa)
    visarecived = mod.VisaRecivedDoc.objects.get(visa=visa.id)
    
    
    context = {
        'page': 'مشخصات ویزا',
        'visa': visa,
        'visapayment': visapayment,
        'visarecived': visarecived
    }
    return render(request, 'visa/visaView.html', context)


# payment update
def paymentUpdate(request, pay_id):
    context = {'page' : 'آمار مصرف'}
    return render(request, 'office/paymentUpdate', context)


# customer list
def customerList(request):
    context= {'page': 'لیست مشتریان'}
    return render(request, 'visa/customerList.html', context)


# visa list update cancel save payed approved search engine

# visa update 
def visaUpdate(request,visa_id):
    context = {}
    visa = mod.Visa.objects.get(id = visa_id)
    reciveddoc = mod.VisaRecivedDoc.objects.get(visa = visa)     
    visaPayment = mod.visaPayment.objects.get(visa = visa)
    
    if request.method == 'POST':
        visaType = request.POST.get('visaType_txt')
        customer = request.POST.get('customer_txt')
        recivedDoc = request.POST.get('recivedDoc_txt')  # Assuming you have a file input field with name 'recived_doc'
        blockAddress = request.POST.get('blockAddress_txt')
        blockImage = request.FILES.get('block_img')  # Assuming you have a file input field with name 'block_image'
        payed = request.POST.get('payed_txt')
        emailBy = request.POST.get('emailBy_txt')
        price = request.POST.get('price_txt')
        money = request.POST.get('money_txt')
        customer = request.POST.get('customer_txt')
        dbcustomer = mod.Customer.objects.get(id= customer)
        dbvisatype = mod.VisaType.objects.get(id= visaType)
        dbemailBy = mod.OurEmail.objects.get(id = emailBy)
        dbmoney = mod.Money.objects.get(id = money)
        
        visa.visaType = dbvisatype
        visa.customer = dbcustomer
        visa.emailby = dbemailBy
        visa.money = dbmoney
        visa.price = price
            
       
        reciveddoc.visa = visa
        reciveddoc.Document = recivedDoc
    
       
        visaPayment.visa = visa
        visaPayment.payed = payed
        visaPayment.blockAddress = blockAddress
        if blockImage:
             if visaPayment.blockImage:
        # If a file is already associated, delete it before assigning the new file
                 visaPayment.blockImage.delete()
                 visaPayment.blockImage = blockImage
        
        visa.save()
        reciveddoc.save()
        visaPayment.save()
        return redirect('/visaList')        
    context['visa'] = mod.Visa.objects.get(id = visa_id)
    context['reciveddoc'] = mod.VisaRecivedDoc.objects.get(visa = visa)
    context['visaPayment'] = mod.visaPayment.objects.get(visa = visa)
    
    context['emailby'] = mod.OurEmail.objects.all()
    context['customers'] = mod.Customer.objects.all().reverse()
    context['visatype'] = mod.VisaType.objects.all()
    context['money'] = mod.Money.objects.all()
    context ['page'] = 'اپدیت ویزا'
    return render(request, 'visa/visaupdate.html',context)

def customerUpdate(request,customer_id):
    context = {}
    context['page'] = 'آپدیت ویزا'
    return render(request,'visa/customerUpdate.html',context)


def registerPayment(request,visa_id):
    context = {}
    registerPayment = None
    context['page'] = "تمدید حالت"
    visa = mod.Visa.objects.get(id = visa_id)
    try:
        registerPayment = mod.registerPayed.objects.get(visa = visa)
    except:
        pass
    
    if registerPayment:
        context['registerPayment'] = registerPayment
    context['visa'] = visa
    money = mod.Money.objects.all()
    cuspay = mod.visaPayment.objects.get(visa = visa_id)
    context['cupay'] = cuspay.payed
    context['money'] = money
    if request.method == 'POST':
        payed = request.POST.get('payed_txt')
        cupayed = request.POST.get('cupayed_txt')
        remoney = request.POST.get('money_txt')
        isapproved = request.POST.get('isapproved_txt')
        isrejected = request.POST.get('isrejected_txt')
        iscomplate = request.POST.get('iscomplate_txt') 
        cuspay.payed = cupayed
        cuspay.save()
        if registerPayment:
            registerPayment.visa = visa
            registerPayment.payed = payed
            registerPayment.money = mod.Money.objects.get(id = remoney)
            registerPayment.save()
        else:
            try:
                mod.Money.objects.get(id = remoney)
                newregisterPayment = mod.registerPayed(
                visa = visa,
                payed = payed,
                money = mod.Money.objects.get(id = remoney) if remoney != 0 else None
                )
                newregisterPayment.save()
            except:
                pass
            
        if isapproved == 'on':
            visa.isapproved = True
            visa.isrejected = False
        else:
            visa.isapproved = False
            
        if isrejected == 'on':
            visa.visapdf.delete()
            visa.isrejected = True
            visa.isapproved = False
        else:
            visa.isrejected = False
        if iscomplate == 'on':
            if visa.isapproved:
                visapdf = None
                try:
                    visapdf = request.FILES['visapdf_file']
                except:
                    pass
                if visapdf != None:
                    if visa.visapdf == None:
                        visa.visapdf = visapdf
                        visa.iscomplate = True
                    else:
                        visa.visapdf.delete()
                        visa.visapdf = visapdf
                        visa.iscomplate = True
                
                else:
                    if visa.visapdf != None:
                        visa.iscomplate = True
                    else:
                        visa.iscomplate = False
            elif visa.isrejected:
                visa.iscomplate = True
            else:
                pass
        else:
            visa.iscomplate = False
        visa.save()
        
        return redirect('/visaList')
    else:
        if visa.isapproved ==True:
            context['approve'] = "checked"
        if visa.isrejected ==True:
            context['reject'] = "checked"
        if visa.iscomplate ==True:
            context['complate'] = "checked"
    return render(request,'visa/registerpayment.html',context)

def visaStatistic(request):
    context = {}
    context['page'] = 'آمار ویزا ها'
    total_price = 0
    total_ofpay = 0
    total_cupay = 0 
    if request.method == 'GET':
         Fvtype = request.GET.get('vtype_txt')
         if Fvtype:
           if Fvtype == '0':
               visas = mod.Visa.objects.all()
               context['records'] = visaacountingList(visas)
               for i in context['records']:
                   total_price += i['visa_price']
                   total_cupay +=i['cupay']
                   total_ofpay +=i['ofpay']
              
               context['total_ofpay'] = total_ofpay
               context['total_cupay_pay'] = total_cupay
               context['percentage_cupay_pay'] = round(context['total_cupay_pay'] * 100 / total_price,2)
               context['total_price'] = total_price
               context['percentage_ofpay'] = round(total_ofpay * 100 / total_price,2)
               context['total_cupay'] = total_price - total_cupay
               context['percentage_cupay'] = round(context['total_cupay'] * 100 /total_price,2)
               context['mafad'] = total_cupay - total_ofpay
               context['mafad_min'] = 'text-white bg-danger' if round(context['mafad'] * 100 / total_price,2) < 0 else 'bg-warning'
               context['percentage_mafad'] = abs(round(context['mafad'] * 100 / total_price,2))
           else:
                 visas = mod.Visa.objects.filter(visaType = Fvtype)
                 context['records'] = visaacountingList(visas)
                 for i in context['records']:
                   total_price += i['visa_price']
                   total_cupay +=i['cupay']
                   total_ofpay +=i['ofpay']
                 
                 context['total_ofpay'] = total_ofpay
                 context['total_cupay_pay'] = total_cupay
                 context['percentage_cupay_pay'] = round(context['total_cupay_pay'] * 100 / total_price,2)
                 context['total_price'] = total_price
                 context['percentage_ofpay'] = round(total_ofpay * 100 / total_price,2)
                 context['total_cupay'] = total_price - total_cupay
                 context['percentage_cupay'] = round(context['total_cupay'] * 100 /total_price,2)
                 context['mafad'] = total_cupay - total_ofpay
                 context['mafad_min'] = 'text-white bg-danger' if round(context['mafad'] * 100 / total_price,2) < 0 else 'bg-warning'
                 context['percentage_mafad'] = abs(round(context['mafad'] * 100 / total_price,2))
         else:
              context['records'] = visaacountingList(mod.Visa.objects.all())
              for i in context['records']:
                   total_price += i['visa_price']
                   total_cupay +=i['cupay']
                   total_ofpay +=i['ofpay']

              context['total_ofpay'] = total_ofpay
              context['total_cupay_pay'] = total_cupay
              context['percentage_cupay_pay'] = round(context['total_cupay_pay'] * 100 / total_price,2)
              context['total_price'] = total_price
              context['percentage_ofpay'] = round(total_ofpay * 100 / total_price,2)
              context['total_cupay'] = total_price - total_cupay
              context['percentage_cupay'] = round(context['total_cupay'] * 100 /total_price,2)
              context['mafad'] = total_cupay - total_ofpay
              context['mafad_min'] = 'text-white bg-danger' if round(context['mafad'] * 100 / total_price,2) < 0 else 'bg-warning'
              context['percentage_mafad'] = abs(round(context['mafad'] * 100 / total_price,2))
    context['vtype'] = mod.VisaType.objects.all()
    context['visastatistic'] = ' text-warning sub-bg '
    return render(request,'visa/visastatistic.html',context)


def mafad(price,ofpay,cupay,visa_id):
    visatype = mod.VisaType.objects.get(visa = visa_id)
    if cupay > visatype.price:
        return cupay - visatype.price
    else:
        return cupay - ofpay
    
    
def visaacountingList(visas):
    records = []
    for visa in visas:
        record = {}

        # Retrieve visa payment
        cupay = mod.visaPayment.objects.get(visa=visa)

        # Retrieve optional payment
        try:
            ofpay = mod.registerPayed.objects.get(visa=visa)
        except mod.registerPayed.DoesNotExist:
            ofpay = None

        # Assign values to the record dictionary
        record['visa_id'] = visa.id
        record['visa_customer'] = visa.customer
        record['visa_type'] = visa.visaType
        record['visa_price'] = visa.price
        record['cupay'] = cupay.payed


        if ofpay:
            record['ofpay'] = ofpay.payed

        else:
            record['ofpay'] = 0.0
           
        record['mafad'] = mafad(visa.price, record['ofpay'] , cupay.payed,visa.id)
        record['remain'] = visa.price - cupay.payed
        
        records.append(record) 
    return records


def employeeRegister(request): 
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        lname = request.POST.get('lname_txt')
        userType = request.POST.get('type_txt')
        if 'profile_img' in request.FILES:
            profileImage = request.FILES['profile_img']
        else:
            profileImage = None
        phone = request.POST.get('phone_txt')
        email = request.POST.get('email_txt')
        username = request.POST.get('username_txt')
        password = request.POST.get('password1_txt')
        repassword = request.POST.get('password2_txt')
        if password == repassword:
            if mod.CustomUser.objects.filter(email=email).exists():
                context['email_error'] = 'email is already exists'
                print('email is already exists')
                return render(request, 'account/employee_registeration.html', context)
            else:
                username = username.lower()
                user = mod.CustomUser.objects.create_user(
                    username=username, email=email, password=password)
                user.first_name = name
                user.last_name = lname
                user.profile_image = profileImage
                user.user_type = userType
                user.save()
                if userType == 'Boss':
                    Boss_obj = mod.Boss(
                        admin=user,
                        phone=phone,
                    )
                    Boss_obj.save()
                    return redirect('/')
                elif userType == 'Employee':
                    Employee_obj = mod.Employee(
                        admin=user,
                        phone=phone
                    )
                    Employee_obj.save()
                elif userType == 'Manager':
                    Manager_obj = mod.Manager(
                        admin=user,
                        phone=phone,
                    )
                    Manager_obj.save()
                return redirect('/')
        else:
            context['password_error'] = 'Password is not match'
            print('password mismatch')
            return render(request, 'account/employee_registeration.html', context)
    context['page'] = 'راجستر کارمند'
    return render (request, 'account/employee_registeration.html')
