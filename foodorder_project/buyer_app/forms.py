from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class BuyerRegisterForm(UserCreationForm):
    # No need to add 'user_type' field since it defaults to 'buyer'
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class SellerRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, initial='seller', widget=forms.HiddenInput())
    logo = forms.ImageField(required=False)  # Add image field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','logo', 'user_type']



class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password",
    )