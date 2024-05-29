from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import ResetPasswordView, PasswordResetDoneView

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', LoginView.as_view(template_name='accounts/sign_in.html'), name='sign_in'),
    path('logout/', LogoutView.as_view(next_page='sign_in'), name='logout'),
    path('users/', views.users, name='users'),
    path('add-user/', views.users, name='add_user'),  # Add URL pattern for adding user
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),  # Add URL pattern for deleting user
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset_form'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
]