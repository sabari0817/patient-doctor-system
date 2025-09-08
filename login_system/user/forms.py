from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'status']

class SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = [
            'role', 'first_name', 'last_name', 'profile_pic',
            'username', 'email', 'password1', 'password2',
            'address_line1', 'city', 'state', 'pincode'
        ]


        
