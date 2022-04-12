from django.contrib.auth.models import User
from users.models import Order
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users import shopkeepers

shops = shopkeepers.shops
SHOPS = []
for key,value in shops.items():
    SHOPS.append((value,value))


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class OrderForm(forms.ModelForm):
    shopkeeper_location = forms.ChoiceField(choices=SHOPS)
    class Meta:
        model = Order
        fields = ['file','shopkeeper_location','no_of_copies','black_and_white']

class OTPForm(forms.Form):
    otp = forms.IntegerField()