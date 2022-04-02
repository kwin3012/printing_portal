from django.shortcuts import render,redirect
from users.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def Home(request):
    return render(request,"users/home.html")

def Register(request):
    print(request)
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


    

