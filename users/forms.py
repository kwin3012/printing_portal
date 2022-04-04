from django.contrib.auth.models import User
from users.models import Order
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['file','shopkeeper_email','no_of_copies','black_and_white']