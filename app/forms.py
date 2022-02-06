from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _
from .models import Customer



class CustomerRegistrationForm(UserCreationForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Password'
        }))
    password2 = forms.CharField(
        label='Confirm Password (again)',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Password'
        }))
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Email'
        }))


    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Your UserName'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter Your First Name'}),


        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = CharField(label = _("Password"), strip = False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label= _("Old Password"), strip = False, widget = forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control', 'placeholder':'Enter Your Old Password'}))
    new_password1 = forms.CharField(label= _("New Password"), strip = False, widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control', 'placeholder':'Enter Your New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label= _("Confirm New Password"), strip = False, widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control', 'placeholder':'Confirm Your New Password'}))



class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254,
    widget=forms.EmailInput(attrs={'autocomplete':'email',
    'class':'form-control'
    })
    )

class MySetPasswordForm(SetPasswordForm):
      new_password1 = forms.CharField(label= _("New Password"), strip = False, widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control', 'placeholder':'Enter Your New Password'}), help_text=password_validation.password_validators_help_text_html())
      new_password2 = forms.CharField(label= _("Confirm New Password"), strip = False, widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control', 'placeholder':'Confirm Your New Password'}))



class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}), 
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}),
        'state':forms.Select(attrs={'class':'form-control'}),
        'zipcode':forms.NumberInput(attrs={'class':'form-control'})
        }