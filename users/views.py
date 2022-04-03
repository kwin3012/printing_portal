from django.shortcuts import render,redirect
from users.forms import UserRegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

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

    

