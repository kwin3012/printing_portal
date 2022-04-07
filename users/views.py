from django.shortcuts import render,redirect
from users.forms import UserRegisterForm,LoginForm,OrderForm
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Order
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

# Create your views here.

def Home(request):
    return render(request,"users/home.html")

def Register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
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

                shopkeeper_email = form.cleaned_data.get('shopkeeper_email')
                shopkeeper_location = shopkeeper_email

                file = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(file.name,file)
                file_url = fs.url(filename)

                no_of_copies = form.cleaned_data.get('no_of_copies')
                black_and_white = form.cleaned_data.get('black_and_white')

                cost=100

                order = Order(
                    user=user,
                    shopkeeper_email=shopkeeper_email,
                    shopkeeper_location=shopkeeper_location,
                    file=filename,
                    no_of_copies=no_of_copies,
                    black_and_white=black_and_white,
                    cost=cost,
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

    





    

