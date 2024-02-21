from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Inspection
from django.shortcuts import render
from brand.models import BrandProfile
from product.models import Product

def inspection_list(request):
    brand_profiles = BrandProfile.objects.order_by('last_inspected_date')
    brands_info = []
    for brand_profile in brand_profiles:
        brands_info.append({
            'user': brand_profile.user.username if brand_profile.user else '',
            'name': brand_profile.name,
            'fssai_no': brand_profile.fssai_no,
            'last_inspected_date': brand_profile.last_inspected_date,
            'id': brand_profile.id  # Add brand_profile id to identify the brand
        })
    
    return render(request, 'inspector/inspection_list.html', {'brands_info': brands_info})


from django.shortcuts import render, get_object_or_404
from .models import BrandProfile

def products_of_brand(request, username):
    # Get the BrandProfile based on the unique username
    brand_profile = get_object_or_404(BrandProfile, user__username=username)
    
    # Get all products of the particular brand
    products = brand_profile.product_set.all()
    
    return render(request, 'inspector/products_of_brand.html', {'brand_profile': brand_profile, 'products': products})


# inspector/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ReviewForm
from .models import Inspection
from brand.models import BrandProfile
from product.models import Product
from django.utils import timezone

def product_review(request, username, product_id):
    product = get_object_or_404(Product, pk=product_id)
    brand_profile = product.brand
    form = ReviewForm(request.POST or None)
    
    # Get the initial approval status of the product from the database
    initial_approval_status = product.is_approved
    
    if request.method == 'POST':
        if form.is_valid():
            # Save the review
            inspection = form.save(commit=False)
            inspection.product = product
            inspection.brand = brand_profile
            inspection.save()
            # Update the last_inspected_date of BrandProfile
            brand_profile.last_inspected_date = timezone.now()
            brand_profile.save()
            
            # Update is_approved field of the product based on inspector's decision
            is_approved = request.POST.get('is_approved')  # Retrieve value from form
            if is_approved == 'approved':
                product.is_approved = True
            else:
                product.is_approved = False
            product.save()
            
            return redirect(reverse('inspection-list'))
    
    return render(request, 'inspector/product_review.html', {'product': product, 'brand_profile': brand_profile, 'form': form, 'initial_approval_status': initial_approval_status})

def inspection_home(request):
    # Your view logic here
    return render(request, 'inspector/inspection_home.html')