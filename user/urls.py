from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from .views import login_view, register_view, reg_otp_view

urlpatterns = [
    path('signin/', login_view, name='login'),
    path('signup/', register_view, name='register'),
    path('signup/otp', reg_otp_view, name='otp'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('reset_password/', PasswordResetView.as_view(), name="reset_password"),
    path('reset_pass_sent/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_pass_complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
