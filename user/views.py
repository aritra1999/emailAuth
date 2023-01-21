from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import OTPLog
from .email import email_message
import random


def login_view(request):
    context = {
        'title': 'Sign In'
    }

    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context['login_error'] = "Invalid credentials!"
    return render(request, 'user/login.html', context)


def register_view(request):
    context = {
        'title': 'Sign Up',
        'reg_errors': [],
    }
    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2'):
            if User.objects.filter(email=request.POST.get('email')).exists():
                context["reg_errors"].append("Email already in use!")

            else:
                request.session['user_type'] = request.POST.get('user_type')
                request.session['f_name'] = request.POST.get('f_name')
                request.session['l_name'] = request.POST.get('l_name')
                request.session['email'] = request.POST.get('email')
                request.session['password'] = request.POST.get('password1')

                try:
                     otp = OTPLog.objects.get(email=request.POST.get('email')).otp
                except:
                    otp = random.randint(100000, 999999)
                    OTPLog.objects.create(email=request.POST.get('email'), otp=otp).save()

                message = 'Your OTP is: ' + str(otp)
                email_message(request.POST.get('email'), 'Registration OTP', message)

                return redirect("/auth/signup/otp")
        else:
            context["reg_errors"].append("Passwords don't match!")
    return render(request, 'user/register.html', context)


def reg_otp_view(request):
    context = {
        'title': 'OTP Verification',
        'email': request.session['email']
    }

    if request.POST == "GET":
        print("Resend OTP")

    print(OTPLog.objects.get(email=request.session['email']).otp)
    if request.method == "POST":
        otp = OTPLog.objects.get(email=request.session['email'])
        if int(request.POST.get('otp')) == int(otp.otp):
            User.objects.create_user(
                username=request.session['email'],
                first_name=request.session['f_name'],
                last_name=request.session['l_name'],
                email=request.session['email'],
                password=request.session['password']
            )

            user = authenticate(request, username=request.session['email'], password=request.session['password'])

            if user is not None:
                login(request, user)
            return redirect('/')
        else:
            context['error'] = "Wrong OTP"
    return render(request, 'user/otp.html', context)
