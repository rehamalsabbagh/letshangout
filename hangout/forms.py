from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields= ['first_name','last_name','username','email','password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields= ['profile_image','profile_bio']


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','caption']

        
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())