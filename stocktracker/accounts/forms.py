from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model



class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True, help_text='Required. Enter your phone number.')
    account_key = forms.CharField(max_length=15, required=True, help_text='Required. Enter your user key.')

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'phone', 'account_key']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'
        self.fields['phone'].help_text = 'Required. Enter your phone number.'
        self.fields['account_key'].help_text = 'Required. Enter your user key.'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'border-radius: 25px; padding: 10px;'
            field.help_text = None  # Remove default help texts


class SignInForm(AuthenticationForm):
     def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'border-radius: 25px; padding: 10px;'
            field.help_text = None  # Remove default help texts


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2', 'account_key', 'phone')

class ResetPasswordView(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordView, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['style'] = 'border-radius: 25px; padding: 10px;'

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'border-radius: 25px; padding: 10px;', 'placeholder': 'New password'})
    )
    new_password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'border-radius: 25px; padding: 10px;', 'placeholder': 'Confirm new password'})
    )