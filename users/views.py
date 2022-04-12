from cmath import log
from django.shortcuts import render,redirect
from users.forms import UserRegisterForm,LoginForm,OrderForm,OTPForm
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Order
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from users import shopkeepers
from random import randint

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
                fs = FileSystemStorage()
                filename = fs.save(file.name,file)
                file_url = fs.url(filename)

                no_of_copies = form.cleaned_data.get('no_of_copies')
                black_and_white = form.cleaned_data.get('black_and_white')

                cost=100

                #generating 6 digit random otp
                otp = randint(100000,999999)

                order = Order(
                    user=user,
                    shopkeeper_email=shopkeeper_email,
                    shopkeeper_location=shopkeeper_location,
                    file=filename,
                    no_of_copies=no_of_copies,
                    black_and_white=black_and_white,
                    cost=cost,
                    otp=otp,
                )

                order.save()

                messages.success(request,f'Order Placed Successfully!')
                return redirect('home')
            else:
                messages.error(request,f'Unable to fetch file')

        else:
            print(form.errors)
            messages.error(request,f'Something went wrong!')

    form = OrderForm()
    return render(request,'users/place_order.html',{'form':form})

@login_required
def Order_History(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    orders = Order.objects.filter(user=user).order_by('-date_ordered')
    return render(request,'users/order_history.html',{'orders':orders})

@login_required
def Recent_Orders(request):
    shopkeeper_email = request.user.email
    shopkeepers_orders = Order.objects.filter(shopkeeper_email=shopkeeper_email,printing_status=False).order_by('date_ordered')
    
    return render(request,'users/recent_orders.html',{'orders':shopkeepers_orders})
    
@login_required
def Status_Change(request,order_id):
    order = Order.objects.get(id=order_id)
    order.printing_status = True
    order.save()

    messages.success(request,f'We will inform {order.user.username} to collects his/her documents!')
    return redirect('recent_orders')


@login_required
def Printed_Orders(request):
    form = OTPForm
    shopkeeper_email = request.user.email
    shopkeepers_orders = Order.objects.filter(shopkeeper_email=shopkeeper_email,printing_status=True).order_by('date_ordered')
    
    return render(request,'users/printed_orders.html',{'orders':shopkeepers_orders,'form':form})

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

def Completed_Orders(request):
    shopkeeper_email = request.user.email
    orders = Order.objects.filter(shopkeeper_email=shopkeeper_email,completed_status=True)
    return render(request,'users/completed_orders.html',{'orders':orders})
    






    


    





    

