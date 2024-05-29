from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, SignInForm
from django.contrib.auth.decorators import login_required
from .models import Account # Import your User model if it's customized
from .forms import AccountCreationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomSetPasswordForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Replace with your home page URL name
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Replace with your home page URL name
    else:
        form = SignInForm()
    return render(request, 'accounts/sign_in.html', {'form': form})


@login_required
def users(request):
    add_user_form = AccountCreationForm(request.POST or None)
    if request.method == 'POST' and add_user_form.is_valid():
        add_user_form.save()
        return redirect('users')

    all_users = Account.objects.all()
    return render(request, 'accounts/users.html', {'users': all_users, 'add_user_form': add_user_form})


@login_required
def delete_user(request, user_id):
    user = Account.objects.get(id=user_id)
    user.delete()
    return redirect('users')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(PasswordResetView):
    form_class = CustomSetPasswordForm

def send_test_email():
    send_mail(
        'Test Email',
        'This is a test email sent from Django.',
        settings.DEFAULT_FROM_EMAIL,
        ['charlsonkent@gmail.com'],
        fail_silently=False,
    )