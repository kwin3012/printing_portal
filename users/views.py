from cmath import log
from django.shortcuts import render,redirect,HttpResponseRedirect
from users.forms import UserRegisterForm,LoginForm,OrderForm,OTPForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Order
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from users import shopkeepers
from random import randint
from PyPDF2 import PdfFileMerger
from django.conf import settings
from reportlab.pdfgen import canvas 
from reportlab.pdfbase import pdfmetrics
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import razorpay

import smtplib , time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

shops = shopkeepers.shops

# Create your views here.

def Home(request):
    return render(request,"users/home.html")

def Register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            #check for shopkeeper
            email = form.cleaned_data['email']
            if shops.get(email) is not None:
                user.is_staff = True
                user.save()

            messages.success(request,f'Successfully Register!')
            return redirect('home')
        else:
            messages.error(request,f'something went wrong!')
    
    form = UserRegisterForm()
    return render(request,"users/register.html",{"form":form})


def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email):
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request,user)
                    messages.success(request,f'Welocme back {user.username}!')
                    return redirect('home')
                else:
                    messages.error(request,f'Password does not matched!')
            else:
                messages.error(request,f'No such Email exists!')
        else:
            messages.error(request,f'Somrthing went wrong!')
    
    form = LoginForm()
    return render(request,'users/login.html',{"form":form})

@login_required
def Logout(request):
    logout(request)
    return redirect('home')

@login_required
def Place_Order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST,request.FILES)
        if form.is_valid():

            if request.FILES['file']:
                user_id = request.user.id
                user = User.objects.get(id=user_id)

            
                shopkeeper_location = form.cleaned_data.get('shopkeeper_location')
                for key,value in shops.items():
                    if value==shopkeeper_location:
                        shopkeeper_email=key
                        break

                file = request.FILES['file']
                no_of_copies = form.cleaned_data.get('no_of_copies')
                black_and_white = form.cleaned_data.get('black_and_white')
                
                # this block code create a single page pdf which contains the name and email
                # of user so that shopkeeper correctly indentifies the pdf at the time of completion.
                os.chdir(settings.MEDIA_ROOT)
                pdf_name = user.email + ".pdf"
                pdf = canvas.Canvas(pdf_name)
                pdf.setFont("Courier-Bold", 36)
                pdf.drawCentredString(300, 590, user.username)
                pdf.setFont("Courier-Bold", 24)
                pdf.drawCentredString(290,500, user.email)
                pdf.save()
                
                merger = PdfFileMerger()
                merger.append(file)
                merger.append(pdf_name)
                no_of_pages = len(merger.pages)

                # the order number over here will not be seen to the user and for shopkeepr it will shown
                # but kind of useless. Differentiating filename just help the system to store each uniquely. 
                order_number = len(Order.objects.all())
                new_file_name = user.email + str(order_number + 1) + ".pdf"
                merger.write(new_file_name)
                merger.close()

                BLACK_WHITE_COST = 1
                COLOR_COST = 10

                if black_and_white:
                    cost=BLACK_WHITE_COST
                else:
                    cost=COLOR_COST
                cost = cost*no_of_copies*no_of_pages

                #generating 6 digit random otp
                # otp = randint(100000,999999)
                otp=1

                # the file name attribute is just for reference for user in order history.
                order = Order(
                    user=user,
                    shopkeeper_email=shopkeeper_email,
                    shopkeeper_location=shopkeeper_location,
                    file=new_file_name,
                    file_name = file.name,
                    no_of_copies=no_of_copies,
                    black_and_white=black_and_white,
                    cost=cost,
                    otp=otp,
                )

                order.save()

                return HttpResponseRedirect(reverse('gateway1'))
                # messages.success(request,f'Order Placed Successfully!')
                # return redirect('home')
            else:
                messages.error(request,f'Unable to fetch file')

        else:
            print(form.errors)
            messages.error(request,f'Something went wrong!')

    form = OrderForm()
    return render(request,'users/place_order.html',{'form':form})

@login_required
def Gateway1(request):
    if request.method == "POST":
        email = request.user.email
        order = Order.objects.filter(user=request.user).last()
        cost = order.cost*100
        client = razorpay.Client(auth = (settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create({'amount':cost, 'currency': 'INR', 'payment_capture':'1'})
        order.payment_id = payment['id']
        order.save()
        return render(request,'users/payment.html',{'payment':payment,'user':request.user})
    return render(request,'users/payment.html')

@login_required
def Gateway2(request,order_id):
    if request.method == "POST":
        order = Order.objects.filter(id=order_id)
        cost = order.cost*100
        client = razorpay.Client(auth = (settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create({'amount':cost, 'currency': 'INR', 'payment_capture':'1'})
        order.payment_id = payment['id']
        order.save()
        return render(request,'users/payment.html',{'payment':payment,'user':request.user})
    return render(request,'users/payment.html')

@login_required
@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        for key, val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        order = Order.objects.filter(payment_id = order_id).first()
        order.payment_status = True
        order.save()
        messages.success(request,f'Your order has been placed.')
    return render(request, 'users/success.html')

@login_required
def Order_History(request):
    orders = Order.objects.filter(user=request.user,payment_status=True).order_by('-date_ordered')
    return render(request,'users/order_history.html',{'orders':orders})

@login_required
def Order_Pending(request):
    orders = Order.objects.filter(user=request.user,payment_status=False).order_by('-date_ordered')
    return render(request,'users/order_pending.html',{'orders':orders})

@login_required
def Recent_Orders(request):
    shopkeeper_email = request.user.email
    shopkeepers_orders = Order.objects.filter(shopkeeper_email=shopkeeper_email,printing_status=False,payment_status=True).order_by('date_ordered')
    
    return render(request,'users/recent_orders.html',{'orders':shopkeepers_orders})
    
@login_required
def Status_Change(request,order_id):
    order = Order.objects.get(id=order_id)

    # for sending email to the customer.
    s = smtplib.SMTP("smtp-mail.outlook.com",587)
    s.starttls()
    s.login("PrintingPortal.IITG@outlook.com","Printingdocuments@123")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "DOCUMENTS PRINTED!"
    msg["From"] = "PrintingPortal.IITG@outlook.com"
    msg["To"] = order.user.email
    text = f"HEY {order.user.username}! Your documents: {order.file_name}, uploaded to us has been printed. Kindly Collect them using this as OTP: {order.otp}"
    msg.attach(MIMEText(text,"plain"))
    s.sendmail("PrintingPortal.IITG@outlook.com",order.user.email, msg.as_string())
    s.quit()

    order.printing_status = True
    order.save()

    messages.success(request,f'We will inform {order.user.username} to collects his/her documents!')
    return redirect('recent_orders')


@login_required
def Printed_Orders(request):
    form = OTPForm
    shopkeeper_email = request.user.email
    shopkeepers_orders = Order.objects.filter(shopkeeper_email=shopkeeper_email,printing_status=True,completed_status=False).order_by('date_ordered')
    
    return render(request,'users/printed_orders.html',{'orders':shopkeepers_orders,'form':form})

@login_required
def Check_OTP(request,order_id):
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            order = Order.objects.get(id=order_id)
            if order.otp == otp:
                order.completed_status = True
                order.save()
                messages.success(request,f'Congratualations You have completed an order id {order.id}!')
            else:
                messages.error(request,f'The OTP did not matched got Order id {order.id}.')
        else:
            messages.error(request,f'Something went wrong!')
        return redirect('printed_orders')

@login_required
def Completed_Orders(request):
    shopkeeper_email = request.user.email
    orders = Order.objects.filter(shopkeeper_email=shopkeeper_email,completed_status=True).order_by('-date_ordered')
    return render(request,'users/completed_orders.html',{'orders':orders})

@login_required
def Download(request,order_id):
    order = Order.objects.get(id=order_id)
    filepath = order.file.path
    os.chdir(settings.MEDIA_ROOT)
    if os.path.exists(filepath):
        print(filepath)
        response = FileResponse(open(filepath, 'rb'))
        return response
    else:
        messages.error(request,f'Document Not Found for Order Id {order.id}')
        return redirect('recent_orders')




    






    


    





    

