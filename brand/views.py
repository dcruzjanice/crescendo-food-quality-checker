# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import BrandProfile
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def brand_home(request):
    return render(request, 'brand_home.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import BrandProfile
from django.urls import reverse
from django.contrib.auth.models import User


from .fssai_validator import validate_fssai


def brand_login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, 'User not found.')
            return redirect(reverse('brand_login_attempt'))
        
        brand_profile_obj = BrandProfile.objects.filter(user=user_obj).first()

        if brand_profile_obj is None:
            messages.error(request, 'Brand profile not found.')
            return redirect(reverse('brand_login_attempt'))

        if not brand_profile_obj.is_verified:
            messages.error(request, 'Profile is not verified or approved by the admin.')
            return redirect(reverse('brand_login_attempt'))

        if not brand_profile_obj.is_approved:
            messages.error(request, 'Profile is not yet approved by the admin.')
            return redirect(reverse('brand_login_attempt'))

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong password.')
            return redirect(reverse('brand_login_attempt'))

        login(request, user)
        return redirect(reverse('brand_home'))

    return render(request, 'brand_login.html')

from product.models import Product

@login_required(login_url='/brand/login')
def brand_home(request):
    brand_profile = request.user.brandprofile
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        product_type = request.POST.get('product_type')
        price = request.POST.get('price')
        food_additives = request.POST.get('food_additives')
        #food_preservatives = request.POST.get('food_preservatives')
        image = request.FILES.get('image')  # Get the uploaded image file
        
        # Check if the file type is JPG or PNG
        if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            messages.error(request, 'Please upload a JPG or PNG file.')
            return redirect('brand_home')
        
        product = Product.objects.create(
            brand=brand_profile,
            name=name,
            category=category,
            product_type=product_type,
            price=price,
            food_additives=food_additives,
            #food_preservatives=food_preservatives,
            image=image,  # Save the uploaded image
            is_approved=False
        )

        messages.success(request, 'Product details added successfully. It is now under approval.')
        return redirect('brand_home')

    else:
        products = Product.objects.filter(brand=brand_profile)
        return render(request, 'brand_home.html', {'products': products, 'brand_profile': brand_profile, 'messages': messages.get_messages(request)})



from django.contrib.auth import logout

def brand_logout_view(request):
    logout(request)
    return redirect(reverse('brand_login_attempt'))

def brand_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            auth_token = str(uuid.uuid4())
            brand_profile_obj, _ = BrandProfile.objects.get_or_create(user=user)
            brand_profile_obj.auth_token = auth_token
            brand_profile_obj.save()
            send_brand_password_reset_email(email, auth_token)
            messages.success(request, 'Password reset link sent to your email.')
            return redirect(reverse('brand_login_attempt'))

        else:
            messages.error(request, 'No user found with this email.')
            return redirect('password_reset')

    return render(request, 'brand_password_reset.html')

def send_brand_password_reset_email(email, token):
    subject = 'Password Reset'
    message = f'Click the link to reset your password: http://127.0.0.1:8000/brand/reset_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # Deactivate older tokens
    BrandProfile.objects.filter(user__email=email).exclude(auth_token=token).delete()

    send_mail(subject, message, email_from, recipient_list)

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BrandProfile
from django.conf import settings

def brand_password_reset_confirm(request, auth_token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            brand_profile_obj = BrandProfile.objects.filter(auth_token=auth_token).first()
            if brand_profile_obj:
                user = brand_profile_obj.user
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('/brand/login')
            else:
                messages.error(request, 'Invalid token.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'brand_password_reset_confirm.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import BrandProfile
from .fssai_validator import validate_fssai  # Import the validation function
import uuid

def brand_register_attempt(request):
    error_message = None  # Initialize error message variable
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        address = request.POST.get('address')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        fssai_no = request.POST.get('fssai_no')
        year = request.POST.get('year')  # Retrieve year from POST data

        try:
            if User.objects.filter(username=username).exists():
                error_message = 'Username is taken.'
                raise Exception('Username is taken.')

            if User.objects.filter(email=email).exists():
                error_message = 'Email is taken.'
                raise Exception('Email is taken.')

            # Validate FASSAI number
            is_valid, message = validate_fssai(fssai_no, state, year)
            if not is_valid:
                error_message = message
                raise Exception(message)

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            brand_profile_obj = BrandProfile.objects.create(user=user_obj, name=name, address=address,
                                                            district=district, pincode=pincode, state=state,
                                                            fssai_no=fssai_no, year=year,
                                                            is_validated=True)  # Set is_validated to True
            brand_profile_obj.save()

            auth_token = str(uuid.uuid4())
            brand_profile_obj.auth_token = auth_token
            brand_profile_obj.save()

            # Assuming send_brand_mail_after_registration is defined elsewhere
            send_brand_mail_after_registration(email, auth_token)
            return redirect('brand_token_send')

        except Exception as e:
            print(e)

    return render(request, 'brand_register.html', {'error_message': error_message})


def brand_success(request):
    return render(request, 'brand_success.html')

def brand_token_send(request):
    return render(request, 'brand_token_send.html')

def brand_verify(request, auth_token):
    try:
        brand_profile_obj = BrandProfile.objects.filter(auth_token=auth_token).first()

        if brand_profile_obj:
            if brand_profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/brand/login')
            brand_profile_obj.is_verified = True
            brand_profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/brand/login')
        else:
            return redirect('/brand/error')
    except Exception as e:
        print(e)
        return redirect(reverse('home'))

def brand_error_page(request):
    return render(request, 'brand_error.html')

def send_brand_mail_after_registration(email, token):
    subject = 'Your account needs to be verified'
    message = f'Click on this link to verify and Login: http://127.0.0.1:8000/brand/verify/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
