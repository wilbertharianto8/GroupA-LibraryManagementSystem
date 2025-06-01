from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match.")
        return password2

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'phone_number', 'address', 'profile_picture']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }