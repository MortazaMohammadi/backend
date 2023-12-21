import array
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
from datetime import datetime


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
            try:
                bill = mod.Bill.objects.get(id = 50)
            except:
                bill = None
            if bill != None:
                return redirect('/logout')
            else:
                 return redirect('/bill')
        else:
            context['aut']= 'نام کاربری یا رمز عبور تان اشتباه است.'
    return render(request, 'account/login.html',context)

# logout
def logout_user(request):
    logout(request)
    return redirect('/')

# add payments
@login_required(login_url='/')
def addPayment(request):    
    context = {}
    context['money'] = mod.Money.objects.all()
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
        context['addpay'] = ' text-warning sub-bg ps-3'
        return render(request, 'office/addPayment.html',context)

# payment list and static for payment
@login_required(login_url='/')
def paymentList(request):
    context = {}
    context['money'] = mod.Money.objects.all()
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
                try:
                    filtered_amount = mod.Payment.objects.filter(payment_type__id=i.id).aggregate(filtered_amount=Sum('amount'))['filtered_amount']
                    if filtered_amount ==None:
                        filtered_amount =0
                except TypeError:
                    filtered_amount = 1
                l2.append(i.title)
                l2.append(filtered_amount)
                l2.append(round(filtered_amount*100/total_amount,2))
                l1.append(l2)
            context['eachptype'] = l1
            context['paytype'] = mod.Payment_type.objects.all()
    context['page'] = 'لیست مصارف'
    context['listpay'] = ' text-warning sub-bg ps-3'
    return render(request, 'office/paymentList.html',context)

# Customer Registeration
@login_required(login_url='/')
def customerRegister(request, bill_id,passport_id):
    bill = mod.Bill.objects.get(id = bill_id)
    
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
        try:
            card_image = request.FILES['card_img']
        except:
            card_image = None
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
            passport=passport.upper(),
            profile=profile_image,
            cardImage=card_image,
            passportImage=passport_image
        )
        customer.save()  # Save the customer object to the database
        
        bcv = mod.BCV(
            bill = bill,
            customer = customer
        )
        bcv.save()
        bill.cr = True
        bill.save()
        return redirect('/billCustomer')  # Redirect to a success page
    
    money = mod.Money.objects.all()
    return render(request, 'visa/customerRegister.html', {'page': 'راجستر مشتری','cusregister':' text-warning sub-bg ps-3','money' : money,'bill':bill,'passport':passport_id})

# ------------------==========================================================================================
def qararrdad(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        fname = request.POST.get('fname_txt')
        passport = request.POST.get('passport_txt')
        price = request.POST.get('price_txt')
        phone = request.POST.get('phone_txt')
        payed = request.POST.get('payed_txt')
        type = request.POST.get('type_txt')
        dbtype = mod.qararrtype.objects.get(id = type)
        qararr = mod.qararrdad(
            name = name,
            fname = fname,
            passport = passport.upper(),
            price = price,
            phone = phone,
            payed = payed,
            type = dbtype
        )
        qararr.save()
    context['page'] = 'اضافه قرار داد خط'
    context['qararrdad'] = 'sub-bg text-warning'
    context['list'] = mod.qararrdad.objects.order_by('-id')
    context['type'] = mod.qararrtype.objects.all()
    return render(request, 'qararr/qararrdad.html',context)

def updateqararrdad(request,qararr_id):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        fname = request.POST.get('fname_txt')
        passport = request.POST.get('passport_txt')
        price = request.POST.get('price_txt')
        phone = request.POST.get('phone_txt')
        payed = request.POST.get('payed_txt')
        type = request.POST.get('type_txt')
        dbtype = mod.qararrtype.objects.get(id = type)
        qararr = mod.qararrdad.objects.get(id = qararr_id)
        qararr.name = name
        qararr.fname = fname
        qararr.passport = passport.upper()
        qararr.price = price
        qararr.phone = phone
        qararr.payed = payed
        qararr.type = dbtype
        qararr.save()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    context['page'] = 'اضافه قرار داد خط'
    context['qararrdad'] = 'sub-bg text-warning'
    context['records'] = mod.qararrdad.objects.get(id = qararr_id)
    context['type'] = mod.qararrtype.objects.all()
    return render(request, 'qararr/updateqararrdad.html',context)

def deleteqararrdad(request,qararr_id):
    qararr = mod.qararrdad.objects.get(id = qararr_id)
    qararr.delete()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

def deactiveqararrdad(request,qararr_id):
    qararrdad = mod.qararrdad.objects.get(id = qararr_id)
    qararrdad.active = False
    qararrdad.save()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)


def doneqararrdad(request,qararr_id):
    qararrdad = mod.qararrdad.objects.get(id = qararr_id)
    qararrdad.done = True
    qararrdad.save()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

def listqararrdad(request,active):
    context = {}
    if request.method == 'POST':
        passport = request.POST.get('passport_txt')
        qararrs = mod.qararrdad.objects.filter(passport = passport)
    else:
        if active == 3:
            context['three'] = 'bg-warning'
            qararrs = mod.qararrdad.objects.filter( done = True).order_by('-id')
        elif active == 2:
            context['two'] = 'bg-warning'
            qararrs = mod.qararrdad.objects.filter(active = False).order_by('-id')
        else:
            context['one'] = 'bg-warning'
            qararrs = mod.qararrdad.objects.filter(done = False,active= True).order_by('-id')
    context['list'] = qararrs
    context['page'] = 'لیست قرارداد ها'
    context['qararrdad'] = 'sub-bg text-warning'
    return render(request, 'qararr/listqararrdad.html', context)

def printqararrdad(request,qararr_id):
    qararr = mod.qararrdad.objects.get(id = qararr_id)
    baqi = qararr.price - qararr.payed
    return render(request, 'qararr/printqararrdad.html', {'qararr': qararr,'baqi':baqi})

    
# ----------------------===========================================================================

def billCustomer(request):
    context = {}
    bill = mod.Bill.objects.filter(isdone = True, cv = False)
    context['bill'] = bill
    context['page'] = 'راجستر مشتری'
    context['cusregister'] = ' text-warning sub-bg ps-3'
    return render(request,'visa/bill_customer.html',context)


def crTrue(request,bill_id,passport_id):
    bill = mod.Bill.objects.get(id = bill_id)
    try:
         customer = mod.Customer.objects.get(passport = passport_id)
    except:
         
         return redirect('/customerRegister/'+ str(bill_id) +'/'+str(passport_id))
    bill.cr = True
    bill.save()
    bcv = mod.BCV(
        bill = bill,
        customer = customer
    )
    bcv.save()
    return redirect('/billCustomer')


def deletbcv(request,bcv_id):
    bcv = ''
    

def cvTrue(request,bill_id):
    bill = mod.Bill.objects.get(id = bill_id)
    bill.cv = True
    bill.save()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)


def billVisa(request):
    context = {}
    records = mod.BCV.objects.filter(visa = None)
    context['records'] = records
    context['page'] = 'راجستر ویزا'
    context['visaregister'] = ' text-warning sub-bg ps-3'
    return render(request,'visa/bill_visa.html',context)


def saveBill(request,bill_id):
    bill = mod.Bill.objects.get(id = bill_id)
    otherprice = mod.otherbill.objects.get(id = bill.othertype.id)
    bill.mainprice = otherprice.price
    bill.isdone = True
    bill.cr = True
    bill.cv = True
    bill.save()
    
    return redirect('/bill')
# visa registeration page

@login_required(login_url='/')
def visaRegister(request,bcv_id):
    context = {}
    bcv = mod.BCV.objects.get(id = bcv_id)
    if request.method == 'POST':
        visaType = request.POST.get('visaType_txt')
        customer = request.POST.get('customer_txt')
        try:
             recivedDoc = request.POST.get('recivedDoc_txt')
        except:
            recivedDoc = None# Assuming you have a file input field with name 'recived_doc'
        try:
             blockAddress = request.POST.get('blockAddress_txt')
        except:
            blockAddress = 'وجود ندارد'
        try:
            blockImage = request.FILES.get('block_img')  # Assuming you have a file input field with name 'block_image'
        except:
            blockImage = None
        payed = request.POST.get('payed_txt')
        emailBy = request.POST.get('emailBy_txt')
        price = request.POST.get('price_txt')
        money = request.POST.get('money_txt')
        customer = request.POST.get('customer_txt')
        dbcustomer = mod.Customer.objects.get(id= customer)
        dbvisatype = mod.VisaType.objects.get(id= visaType)
        dbemailBy = mod.OurEmail.objects.get(id = emailBy)
        dbmoney = mod.Money.objects.get(id = money)
        employee = mod.CustomUser.objects.get(id = request.user.id )
        visa = mod.Visa(
            visaType = dbvisatype,
            customer = dbcustomer,
            employee = employee,
            emailby = dbemailBy,
            money = dbmoney,
            price = price,
            bill = bcv.bill
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
        bcv.visa = visa
        bcv.save()
        return redirect('/billVisa')   
    context['money'] = mod.Money.objects.all()
    context['emailby'] = mod.OurEmail.objects.all()
    context['page'] = 'راجستر ویزا'
    context['visaregister'] = ' text-warning sub-bg ps-3'
    context['bcv'] = bcv
    return render(request, 'visa/visaRegister.html',context)

# visa list
def visaList(request):
    context = {}
    if request.method == 'GET':
        passport_txt = request.GET.get('passport_txt')
        
        if passport_txt:
            try:
                customer = mod.Customer.objects.get(passport=passport_txt.upper())
                context['visalisting'] = mod.Visa.objects.filter(customer=customer)
            except mod.Customer.DoesNotExist:
                pass
            
            return render(request, 'visa/visaList.html', context)
    
    context['money'] = mod.Money.objects.all()
    context['visalisting'] = mod.Visa.objects.all()
    context['visaList'] = ' text-warning sub-bg ps-3'
    context['page'] = 'لیست ویزا'
    return render(request, 'visa/visaList.html', context)

# bill print
@login_required(login_url='/')
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
        peopleNo = request.POST.get('people_txt')
        phone = request.POST.get('phone_txt')
        try:
            dbvisatype = mod.VisaType.objects.get(id= visatype)
        except:
          dbvisatype = None
        
        mytype = None
        mytype2 = None
        if dbvisatype:
            mytype = dbvisatype
        else:
            mytype2 = mod.otherbill.objects.get(title = visatype)
        dbmoney = mod.Money.objects.get(id = money)
        billing = mod.Bill(
            name = name,
            reciveddoc = reciveddoc,
            visatype = mytype,
            othertype = mytype2,
            price = price,
            payed = payed,
            money = dbmoney,
            duration = duration,
            peopleNo = peopleNo,
            phone = phone
        )
        billing.save()
        return redirect('/bill#list')
    else:
        pass
    context['bill'] = ' text-warning sub-bg ps-3'
    context['page'] = 'راجستر بل'
    context['billListing'] = mod.Bill.objects.filter(isdone = False)
    context['visaList'] = mod.VisaType.objects.all()
    context['other'] = mod.otherbill.objects.all()
    context['money'] = mod.Money.objects.all()
    return render(request, 'billing/bill.html', context)

# bill print
@login_required(login_url='/')
def billPrint(request, bill_id):
    context = {}
    bill = mod.Bill.objects.get(id = bill_id)
    
    context['remain']=bill.price - bill.payed
    context['bill'] = bill
    
    return render(request, 'billing/billprint.html',context)

# bill delete
@login_required(login_url='/')
def deleteBill(request, bill_id):
    mod.Bill.objects.get(id = bill_id).delete()
    return redirect('/bill#list')

@login_required(login_url='/')
def deactiveBill(request, bill_id):
    bill = mod.Bill.objects.get(id = bill_id)
    bill.isactive = False
    bill.save()
    try:
         visa = mod.Visa.objects.get(bill = bill)
         visa.delete()
         referer = request.META.get('HTTP_REFERER')
    except:
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)
    return redirect(referer)

# bill send for register
@login_required(login_url='/')
def sendBill(request, bill_id):
    bill = mod.Bill.objects.get(id = bill_id)
    bill.isdone = True
    bill.save()
    bcv = mod.BCV(
        bill = bill
    )
    bcv.save
    return redirect('/bill#list')

# bill update
@login_required(login_url='/')
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
        bill.peopleNo = request.POST.get('people_txt')
        mainprice = request.POST.get('mainprice_txt')
        bill.phone = request.POST.get('phone_txt')
      
        
        try:
            bill.visatype = mod.VisaType.objects.get(id= visatype)
        except:
            bill.visatype = None
        try:
           bill.othertype =  mod.otherbill.objects.get(title = visatype) 
        except:
            bill.othertype = None
        if bill.visatype == None:
            otherbill = mod.otherbill.objects.get(title = visatype)
            otherbill.price = mainprice
            otherbill.save()
            bill.mainprice = mainprice
        bill.money = mod.Money.objects.get(id = money)
        bill.duration = request.POST.get('duration_txt')
        bill.save()
        
        return redirect('/bill#list')
    else:
        context['bill'] = bill
        context['visaList'] = mod.VisaType.objects.all()
        context['other'] = mod.otherbill.objects.all()
        context['money'] = mod.Money.objects.all()
    return render(request, 'billing/updateBill.html', context)
    
# visa View 
@login_required(login_url='/')
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
    
    context['money'] = mod.Money.objects.all()
    return render(request, 'visa/visaView.html', context)

# payment update
@login_required(login_url='/')
def paymentUpdate(request, pay_id):
    context = {'page' : 'آمار مصرف'}
    return render(request, 'office/paymentUpdate', context)

# customer list
@login_required(login_url='/')
def customerList(request):
    context= {'page': 'لیست مشتریان'}
    return render(request, 'visa/customerList.html', context)

# visa update 
@login_required(login_url='/')
def visaUpdate(request,visa_id):
    context = {}
    visa = mod.Visa.objects.get(id = visa_id)
    thedate = visa.saveddate
    reciveddoc = mod.VisaRecivedDoc.objects.get(visa = visa)     
    visaPayment = mod.visaPayment.objects.get(visa = visa)
    
    if request.method == 'POST':
        visaType = request.POST.get('visaType_txt')
        customer = request.POST.get('customer_txt')
        try:
            recivedDoc = request.POST.get('recivedDoc_txt')
        except:
            recivedDoc = None # Assuming you have a file input field with name 'recived_doc'
        try:
            blockAddress = request.POST.get('blockAddress_txt')
        except:
            blockAddress = None
        try:
            blockImage = request.FILES.get('block_img')
        except:
            blockImage = None
         # Assuming you have a file input field with name 'block_image'
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
        visa.saveddate = thedate
        print(thedate,'--',visa.saveddate)
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

# register payment
@login_required(login_url='/')
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
    
    cuspay = mod.visaPayment.objects.get(visa = visa_id)
    context['cupay'] = cuspay.payed
    if request.method == 'POST':
        payed = request.POST.get('payed_txt')
        cupayed = request.POST.get('cupayed_txt')
       
        isapproved = request.POST.get('isapproved_txt')
        isrejected = request.POST.get('isrejected_txt')
        iscomplate = request.POST.get('iscomplate_txt') 
        cuspay.payed = cupayed
        cuspay.save()
      
        if visa.Otherdocs == None:
                try:
                     Otherdocs = request.FILES['otherdocs_file']
                except:
                    Otherdocs = None
                
                visa.Otherdocs = Otherdocs
               
        else:
                try:
                     Otherdocs = request.FILES['otherdocs_file']
                except:
                    Otherdocs = None
                if Otherdocs != None:
                    visa.Otherdocs.delete()
                    visa.Otherdocs = Otherdocs
                else:
                    pass
        visa.saveddate = visa.saveddate
        print(visa.Otherdocs)
        visa.save()
        if registerPayment:
            registerPayment.visa = visa
            registerPayment.payed = payed
            
            registerPayment.save()
        else:
            try:
                
                newregisterPayment = mod.registerPayed(
                visa = visa,
                payed = payed,
                
                )
                newregisterPayment.save()
            except:
                pass
            
        if isapproved == 'on':
            visa.isapproved = True
            visa.isrejected = False
            try:
                visapdf = request.FILES['visapdf_file']
            except:
                pass
            if visa.visapdf == None:
                if visapdf in request.FILES:
                    visa.visapdf = visapdf
                else:
                    pass
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
    
    context['money'] = mod.Money.objects.all()
    return render(request,'visa/registerpayment.html',context)

# visa statistic
@login_required(login_url='/')
def visaStatistic(request):
    context = {}
    context['page'] = 'آمار ویزا ها'
    total_price = 0
    total_ofpay = 0
    total_cupay = 0 
    
    context['money'] = mod.Money.objects.all()
    try:
        if request.method == 'GET':
         Fvtype = request.GET.get('vtype_txt')
         moneytype = request.GET.get('money_txt')
         month = request.GET.get('month_txt')
         
         if moneytype:
            totype = mod.Money.objects.get(id = moneytype)
         else:
            totype = mod.Money.objects.get(id = 1)
         if month:
            month = datetime.strptime(month, '%Y-%m')
         else:
            month = datetime.now()
         if Fvtype:
           if Fvtype == '0':
               visas = Visa.objects.filter(saveddate__year=month.year, saveddate__month=month.month)
               context['records'] = visaacountingList(visas)
               for i in context['records']:
                   
                   moneychange(i['visa_price'],i["money_type"],totype.money_type)
                   total_price +=  moneychange(i['visa_price'],i["money_type"],totype)
                   total_cupay += moneychange(i['cupay'],i["money_type"],totype)
                   total_ofpay +=  moneychange(i['ofpay'],i["money_type"],totype)
              
               context['total_ofpay'] = round(total_ofpay,3)
               context['total_cupay_pay'] = round(total_cupay,3)
               context['percentage_cupay_pay'] = round(context['total_cupay_pay'] * 100 / total_price,2)
               context['total_price'] = round(total_price,3)
               context['percentage_ofpay'] = round(total_ofpay * 100 / total_price,2)
               context['total_cupay'] = round(total_price - total_cupay,3)
               context['percentage_cupay'] = round(context['total_cupay'] * 100 /total_price,2)
               context['mafad'] = round(total_cupay - total_ofpay,3)
               context['mafad_min'] = 'text-white bg-danger' if round(context['mafad'] * 100 / total_price,2) < 0 else 'bg-warning'
               context['percentage_mafad'] = abs(round(context['mafad'] * 100 / total_price,2))
           else:
                 visas = mod.Visa.objects.filter(visaType = Fvtype)
                 if len(visas) != 0:
                    context['records'] = visaacountingList(visas)
                    for i in context['records']:
                    
                        moneychange(i['visa_price'],i["money_type"],totype)
                        total_price +=  moneychange(i['visa_price'],i["money_type"],totype)
                        total_cupay += moneychange(i['cupay'],i["money_type"],totype)
                        total_ofpay +=  moneychange(i['ofpay'],i["money_type"],totype)
                    
                    context['total_ofpay'] = round(total_ofpay,3)
                    context['total_cupay_pay'] = round(total_cupay,3)
                    context['percentage_cupay_pay'] = round(context['total_cupay_pay'] * 100 / total_price,2)
                    context['total_price'] = round(total_price,3)
                    context['percentage_ofpay'] = round(total_ofpay * 100 / total_price,2)
                    context['total_cupay'] = round(total_price - total_cupay,3)
                    context['percentage_cupay'] = round(context['total_cupay'] * 100 /total_price,2)
                    context['mafad'] = round(total_cupay - total_ofpay,3)
                    context['mafad_min'] = 'text-white bg-danger' if round(context['mafad'] * 100 / total_price,2) < 0 else 'bg-warning'
                    context['percentage_mafad'] = abs(round(context['mafad'] * 100 / total_price,2))
         else:
              context['records'] = visaacountingList(mod.Visa.objects.all())
              for i in context['records']:
                   
                   moneychange(i['visa_price'],i["money_type"],totype)
                   total_price +=  moneychange(i['visa_price'],i["money_type"],totype)
                   total_cupay += moneychange(i['cupay'],i["money_type"],totype)
                   total_ofpay +=  moneychange(i['ofpay'],i["money_type"],totype)

              context['total_ofpay'] = round(total_ofpay,3)
              context['total_cupay_pay'] = round(total_cupay,3)
              context['percentage_cupay_pay'] = round(context['total_cupay_pay'] * 100 / total_price,2)
              context['total_price'] = round(total_price,3)
              context['percentage_ofpay'] = round(total_ofpay * 100 / total_price,2)
              context['total_cupay'] = round(total_price - total_cupay,3)
              context['percentage_cupay'] = round(context['total_cupay'] * 100 /total_price,2)
              context['mafad'] = round(total_cupay - total_ofpay,3)
              context['mafad_min'] = 'text-white bg-danger' if round(context['mafad'] * 100 / total_price,2) < 0 else 'bg-warning'
              context['percentage_mafad'] = abs(round(context['mafad'] * 100 / total_price,2))
    except:
         return HttpResponseNotFound('<h1 style = "text-align: center"> هیچ ویزای وجود ندارد </h1>')
    context['vtype'] = mod.VisaType.objects.all()
    context['visastatistic'] = ' text-warning sub-bg ps-3'
    return render(request,'visa/visastatistic.html',context)

# employee register
@login_required(login_url='/')
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
        address = request.POST.get('address_txt')
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
                        address = address,
                    )
                    Boss_obj.save()
                    return redirect('/')
                elif userType == 'Employee':
                    Employee_obj = mod.Employee(
                        admin=user,
                        phone=phone,
                        address = address,
                    )
                    Employee_obj.save()
                elif userType == 'Manager':
                    Manager_obj = mod.Manager(
                        admin=user,
                        phone=phone,
                        address = address
                    )
                    Manager_obj.save()
                return redirect('/')
        else:
            context['password_error'] = 'Password is not match'
            print('password mismatch')
            return render(request, 'account/employee_registeration.html', context)
    context['page'] = 'راجستر کارمند'
    
    context['money'] = mod.Money.objects.all()
    return render (request, 'account/employee_registeration.html')

# mafad function ..................................
def mafad(price,ofpay,cupay,visa_id):
    visatype = mod.VisaType.objects.get(visa = visa_id)
    visa = mod.Visa.objects.get(id = visa_id)
    vtype = round(moneychange(visatype.price,visatype.money,visa.money),3)
    
    if cupay > vtype:
        return cupay - vtype
    else:
        return cupay - ofpay 
    
# visa acounting list ............................
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
        record['visa_price'] = round(visa.price , 3)
        record['money_type'] = visa.money
        record['cupay'] = round(cupay.payed , 3)


        if ofpay:
            record['ofpay'] = round(ofpay.payed , 3)

        else:
            record['ofpay'] = 0.0
           
        record['mafad'] = round(mafad(visa.price, record['ofpay'] , cupay.payed,visa.id) , 3)
        record['remain'] = round(visa.price - cupay.payed , 3)
        
        records.append(record) 
    return records

# Notes  
@login_required(login_url='/')
def notes(request):
    context = {}
    
    context['money'] = mod.Money.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        whatfor = request.POST.get('whatfor_txt')
        type = request.POST.get('type_txt')
        amount = request.POST.get('amount_txt')
        money = request.POST.get('money_txt')
        
        note = mod.Notes(
            name = name,
            whatfor = whatfor,
            type = type,
            amount = amount,
            money = mod.Money.objects.get(id = money)
        )
        note.save()
        return redirect('notes')
    
    context['records'] = mod.Notes.objects.all()
    if request.method == 'GET':
        any = request.GET.get('any_txt')
        mytype = request.GET.get('type_txt')
        if mytype == 'همه':
            result = mod.Notes.objects.filter(Q(whatfor__icontains=any) | Q(name__icontains=any) | Q(amount__icontains=any) | Q(date__icontains=any) )
        elif mytype == None:
            result = mod.Notes.objects.all()
        else:
            result = mod.Notes.objects.filter(Q(whatfor__icontains=any) | Q(name__icontains=any) | Q(amount__icontains=any) | Q(date__icontains=any) ,type = mytype)
        context['records'] = result
    
    context['notes'] = ' text-warning sub-bg ps-3'
    return render(request, 'note/notes.html',context)

# money changing ..........................
def moneychange(amount,type, totype):
    type1 = mod.Money.objects.get(id = type.id)
    totype1 = mod.Money.objects.get(money_type = totype)
    afghani = 0.0
    othercurency = 0.0
    if type1.money_type != 'اففانی':
        afghani = amount * type1.sell_amount / type1.amount
        othercurency = afghani * totype1.amount/ totype1.sell_amount
    else:
        othercurency = afghani * totype1.amount/ totype1.sell_amount
    return round(othercurency,3)

# profile update
from django.contrib import messages
def employeeUpdate(request,user_id):  
    context = {}
    context['money'] = mod.Money.objects.all()
    customuser = mod.CustomUser.objects.get(id = user_id)
    myuser = None
    
    try:
        if mod.Boss.objects.get(admin = customuser):
            myuser = mod.Boss.objects.get(admin = customuser)
        elif mod.Employee.objects.get(admin = customuser):
            myuser = mod.Employee.objects.get(admin = customuser)
        else:
            myuser = mod.Manager.objects.get(admin = customuser)
    except:
        pass
    context['myuser'] = myuser
    if request.method == 'POST':
        name = request.POST.get('name_txt')
        lname = request.POST.get('lname_txt')
        if 'profile_img' in request.FILES:
            profileImage = request.FILES['profile_img']
        else:
            profileImage = None
        phone = request.POST.get('phone_txt')
        address = request.POST.get('address_txt')
        email = request.POST.get('email_txt')
        username = request.POST.get('username_txt')
        cupassword = request.POST.get('password0_txt')
        password = request.POST.get('password1_txt')
        repassword = request.POST.get('password2_txt')
        user = authenticate(username=request.user.username,
                            password=cupassword)
        if user is None:
            messages.error(request, 'Current password is incorrect')
            return redirect('/employeeUpdate/'+ str(user_id))
        else:
            if password != repassword:
                messages.error(
                    request, 'new password and confirm password is does not match')
                return redirect('/employeeUpdate/'+ str(user_id))
            else:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully')
               

            user.first_name = name
            user.last_name = lname
            if profileImage:
                user.profile_image.delete()
                user.profile_image = profileImage
            else:
                pass
            user.email = email
            user.username = username
            user.save()
            myuser.phone = phone
            myuser.address = address
            myuser.save()
            return redirect('/bill')
    context['page'] = 'آپدیت کارمند'
    return render(request, 'account/employee_update.html',context)

# money update
def moneyUpdate(request):
    if request.method == 'POST':
        # Retrieve the updated data from the form
        money = request.POST.get('money_txt')
        amount = request.POST.get('amount_txt')
        sell= request.POST.get('sell_txt')

        # Update the record in the database
        record = mod.Money.objects.get(id=money)  # Assuming you have the record ID
        record.amount = amount
        record.sell_amount = sell
        record.save()
        
        referer = request.META.get('HTTP_REFERER')
        # Redirect the user or render a success template
        return redirect(referer)  # Assuming you have a success URL name

def billListing(request):
    context = {}
    myrecords = []
    totalprice = 0
    totalpayed = 0
    totalremain = 0
    totalmafad = 0
    context['Obilltype'] = mod.otherbill.objects.all()
    context['money'] = mod.Money.objects.all()
    if request.method == 'POST':
        
        
        Obilltype = request.POST.get('Obilltype_txt')
        mymoney = request.POST.get('money_txt')
        if Obilltype == '0' :
            if mymoney == '0':
                records = mod.Bill.objects.filter(visatype=None, cr=True, isactive = True).order_by('-id')
            else:
                records = mod.Bill.objects.filter(visatype = None,money = mymoney,cr= True, isactive = True).order_by('-id')
        elif Obilltype == '-1':
            records = mod.Bill.objects.filter(isactive = False,visatype = None)
        else:
            if mymoney == '0':
                records = mod.Bill.objects.filter(visatype=None,othertype = Obilltype, cr=True, isactive = True).order_by('-id')
            else:
                records = mod.Bill.objects.filter(visatype=None,othertype = Obilltype,money = mymoney, cr=True, isactive = True).order_by('-id')
    else:
       records = mod.Bill.objects.filter(visatype=None, cr=True, isactive = True).order_by('-id')
    for record in records:
        reco = {}
        reco['zero'] = record.id
        reco['one'] = record.name
        reco['two'] = record.othertype.title
        reco['three'] = record.price
        reco['four'] = record.payed
        remaining_amount = record.price - record.payed
        reco['five'] = remaining_amount
        reco['money'] = record.money.money_type
        reco['cancel'] = record.isactive
        reco['isprint'] = record.isprint
        myrecords.append(reco)
        totalprice += moneychange(record.price,record.money,'افغانی')
        totalpayed += moneychange(record.payed,record.money,'افغانی')
        totalremain += moneychange(remaining_amount,record.money,'افغانی')
        mafad  = record.payed - record.mainprice
        totalmafad += moneychange(mafad,record.money,'افغانی')
    context['records'] = myrecords
    context["totalprice"] = totalprice
    context['totalpayed'] = totalpayed
    context['totalremain'] = totalremain
    if totalmafad < 0:
        context['mafadcolor'] = 'bg-danger'
    else:
        context['mafadcolor'] = 'bg-warning'
    context['totalmafad'] = totalmafad
    context["totalpriceper"] = 100 
    if totalprice > 0:
        context['totalpayedper'] = round( totalpayed * 100 / totalprice,2)
        context['totalremainper'] = round(totalremain * 100 / totalprice,2)
        context['totalmafadper'] = abs(round(totalmafad * 100 / totalprice,2))
    
    context['page'] = 'بل های ثبت شده'
    context['billlisting'] = ' text-warning sub-bg ps-3'
    return render(request, 'billing/billlisting.html', context)


def isprint(request,bill_id):
    bill = mod.Bill.objects.get(id = bill_id)
    bill.isprint = True
    bill.save()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)
def allbillListing(request):
    context = {}
    myrecords = []
    totalprice = 0
    totalpayed = 0
    totalremain = 0
    totalmafad = 0
    context['Obilltype'] = mod.otherbill.objects.all()
    context['visatype'] = mod.VisaType.objects.all()
    context['money'] = mod.Money.objects.all()
    if request.method == 'POST':
        Obilltype = request.POST.get('Obilltype_txt')
        mymoney = request.POST.get('money_txt')
        if Obilltype == '0' :
            if mymoney == '0':
                records = mod.Bill.objects.filter(cr=True, isactive = True).order_by('-id')
                
            else:
                records = mod.Bill.objects.filter(money = mymoney,cr= True ,isactive = True).order_by('-id')
        elif Obilltype == '-1':
            records = mod.Bill.objects.filter(isactive = False)
        else:
            if mymoney == '0':
                if 'a' in Obilltype:
                    Obilltype = Obilltype[0]
                    records = mod.Bill.objects.filter(othertype = None,visatype = Obilltype,cr = True ,isactive = True).order_by('-id')
                else:
                    Obilltype = Obilltype[0]
                    records = mod.Bill.objects.filter(visatype=None,othertype = Obilltype, cr=True ,isactive = True).order_by('-id')
                
            else:
                try:
                    records = mod.Bill.objects.filter(visatype=None,othertype = Obilltype,money = mymoney, cr=True ,isactive = True).order_by('-id')
                except:
                    records = mod.Bill.objects.filter(visatype=Obilltype,othertype = None,money = mymoney, cr=True ,isactive = True).order_by('-id')

    else:
        
       records = mod.Bill.objects.filter(cr=True ,isactive = True).order_by('-id')
    for record in records:
        reco = {}
        reco['zero'] = record.id
        reco['one'] = record.name
        if record.visatype == None:
            reco['two'] = record.othertype.title
        else:
            reco['two'] = record.visatype.type +' '+ record.visatype.country
        reco['three'] = record.price
        reco['four'] = record.payed
        remaining_amount = record.price - record.payed
        reco['five'] = remaining_amount
        reco['money'] = record.money.money_type
        reco['cancel'] = record.isactive
        reco['isprint'] = record.isprint
        myrecords.append(reco)
        totalprice += moneychange(record.price,record.money,'افغانی')
        totalpayed += moneychange(record.payed,record.money,'افغانی')
        totalremain += moneychange(remaining_amount,record.money,'افغانی')
        mafad  = record.payed - record.mainprice
        totalmafad += moneychange(mafad,record.money,'افغانی')
    context['records'] = myrecords
    context["totalprice"] = totalprice
    context['totalpayed'] = totalpayed
    context['totalremain'] = totalremain
    if totalmafad < 0:
        context['mafadcolor'] = 'bg-danger'
    else:
        context['mafadcolor'] = 'bg-warning'
    context['totalmafad'] = totalmafad
    context["totalpriceper"] = 100 
    if totalprice > 0:
        context['totalpayedper'] = round( totalpayed * 100 / totalprice,2)
        context['totalremainper'] = round(totalremain * 100 / totalprice,2)
        context['totalmafadper'] = abs(round(totalmafad * 100 / totalprice,2))
    
    context['page'] = 'لیست همه بل ها'
    context['billlisting'] = ' text-warning sub-bg ps-3'
    return render(request, 'billing/allbilllisting.html', context)

def billrecycle(request):
    if request.method == 'POST':
        pass

def totalstatistics(request):
    context = {}
    context['money'] = mod.Money.objects.all()
    if request.method == 'GET':
        totalOfficePayement =  mod.Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount']  #np
        otherBillPayeds = mod.Bill.objects.filter(visatype = None, cr = True )
        sumOtherBillPayeds = 0
        sumOtherBillPrice = 0
        sumOtherBillMainPrice = 0
        for item in otherBillPayeds:
            sumOtherBillPayeds += moneychange(item.payed,item.money,'افغانی')
            sumOtherBillPrice += moneychange(item.price,item.money,'افغانی')
            if item.payed > item.mainprice:
                sumOtherBillMainPrice += moneychange(item.mainprice,item.money,'افغانی')
        totalOfVisas = mod.Visa.objects.all()
        sumVisaPrice = 0
        sumVisaPayed = 0
        sumVisaMainprice = 0
        for items in totalOfVisas:
            sumVisaPrice += moneychange(items.price,items.money,'افغانی')
            payment = mod.visaPayment.objects.get(visa = items.id)
            sumVisaPayed += moneychange(payment.payed,items.money,'افغانی')
            try:
                mainprice = mod.registerPayed.objects.get(id =items.id ).payed
            except:
                mainprice = 0
            sumVisaMainprice  += mainprice
   
   
 
        mmoney = request.GET.get('money_txt')
        if mmoney == None:
            mmoney = 1
        mymoney = mod.Money.objects.get(id = mmoney)
        money = mod.Money.objects.get(id = 3)

        context['Vtotalprice'] = round(moneychange(sumVisaPrice,money,mymoney.money_type),2)
        context['Vtotalpayed'] = round(moneychange(sumVisaPayed,money,mymoney.money_type),2)
        context['Vtotalmainprice'] = round(moneychange(sumVisaMainprice,money,mymoney.money_type),2)
        context['totaloffpayment'] = round(moneychange(totalOfficePayement,money,mymoney.money_type),2)
        context['totalbillprice'] = round(moneychange(sumOtherBillPrice,money,mymoney.money_type),2)
        context['totalbillpay'] = round(moneychange(sumOtherBillPayeds,money,mymoney.money_type),2)
        context['totalbillmainprice'] = round(moneychange(sumOtherBillMainPrice,money,mymoney.money_type),2)

        
        context['TotalCuneedpayed'] = round(context['Vtotalprice'] + context['totalbillprice'],2)
        context['TotalOFFneedpayed'] = round(context['totalbillmainprice'] + context['Vtotalmainprice'] + context['totaloffpayment'],2)
        context['TotalCupayed'] = round(context['Vtotalpayed'] + context['totalbillpay'],2)
        context['TotalMafad'] = round(context['TotalCupayed'] - context['TotalOFFneedpayed'],2)
        
        context['perCuNeedpayed'] = 100
        context['perOffNeedpayed'] = round(context['TotalOFFneedpayed'] * 100 / context['TotalCuneedpayed'],2)
        context['perCupayed'] = round(context['TotalCupayed'] * 100 / context['TotalCuneedpayed'],2)
        context['perMafad'] = abs(round(context['TotalMafad'] * 100 / context['TotalCuneedpayed'],2))
        
                
        
        context['perVprice'] = round(context['Vtotalprice'] * 100 / context['TotalCuneedpayed'],2) 
        context['perVpayed'] = round(context['Vtotalpayed'] * 100 / context['TotalCuneedpayed'],2)
        context['perVmainprice'] = round(context['Vtotalmainprice'] * 100 / context['TotalCuneedpayed'],2)
        context['peroffpayment'] = round(context['totaloffpayment'] * 100 / context['TotalCuneedpayed'],2)
        context['perbillprice'] = round(context['totalbillprice'] * 100 / context['TotalCuneedpayed'],2)
        context['perbillpay'] = round(context['totalbillpay'] * 100 / context['TotalCuneedpayed'],2)
        context['perbillmainprice'] = round(context['totalbillmainprice'] * 100 / context['TotalCuneedpayed'],2)

        context['mymoney'] = mymoney
        
    
    context['page'] = 'آمار کلی'
    context['totalstatisticcolor'] = 'sub-bg text-warning'
    return render(request,'amar/totalstatistic.html',context)