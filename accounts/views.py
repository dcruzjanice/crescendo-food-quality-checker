from accounts.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def home(request):
    return render(request , 'home.html')



def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified, check your email.')
            return redirect('/accounts/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')

        login(request, user)
        return redirect(reverse('products_list'))  # Redirect to the products_list page

    # If the request method is not POST, render the login page template
    return render(request, 'login.html') 

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect(reverse('home'))

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
import uuid
from .models import Profile
from django.conf import settings

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            auth_token = str(uuid.uuid4())
            profile_obj, _ = Profile.objects.get_or_create(user=user)
            profile_obj.auth_token = auth_token
            profile_obj.save()
            send_password_reset_email(email, auth_token)
            messages.success(request, 'Password reset link sent to your email.')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'No user found with this email.')
            return redirect('password_reset')

    return render(request, 'password_reset.html')

def send_password_reset_email(email, token):
    subject = 'Password Reset'
    message = f'Click the link to reset your password: http://127.0.0.1:8000/accounts/reset_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Deactivate older tokens
    Profile.objects.filter(user__email=email).exclude(auth_token=token).delete()

    send_mail(subject, message, email_from, recipient_list)


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from django.conf import settings

def password_reset_confirm(request, auth_token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            profile_obj = Profile.objects.filter(auth_token=auth_token).first()
            if profile_obj:
                user = profile_obj.user
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('/accounts/login')
            else:
                messages.error(request, 'Invalid token.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'password_reset_confirm.html')




# views.py
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')  # Added code to get address

        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken.')
                return redirect('register_attempt')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is taken.')
                return redirect('register_attempt')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token, mobile_number=mobile_number, address=address)
            profile_obj.save()

            send_mail_after_registration(email, auth_token)
            return redirect('token_send')

        except Exception as e:
            print(e)

    return render(request, 'register.html')



def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect(reverse('home'))

def error_page(request):
    return  render(request , 'error.html')



def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Click on this link to verify and Login http://127.0.0.1:8000/accounts/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
    