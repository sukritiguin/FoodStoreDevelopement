from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from .models import Vendor

# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_vendor)
def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if vendor_form.is_valid() and user_profile_form.is_valid():
            user_profile_form.save()
            vendor.save()
            messages.success(request, 'Settings updated.')
            return redirect('vendorProfile')
        else:
            # Combine form errors to include profile picture errors
            errors = {}
            errors.update(vendor_form.errors)
            errors.update(user_profile_form.errors)
            # Include profile picture errors specifically
            # errors['profile_picture'] = user_profile_form['profile_picture'].errors
            # Add error message to messages framework
            messages.error(request, 'Invalid Form.')
    else:
        vendor_form = VendorForm(instance=vendor)
        user_profile_form = UserProfileForm(instance=profile)
        errors = {}

    context = {
        'vendor_form': vendor_form,
        'profile_form': user_profile_form,
        'profile': profile,
        'vendor': vendor,
        'errors': errors,  # Include errors in context
    }
    return render(request, 'vendor/vendorProfile.html', context=context)

def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if vendor_form.is_valid() and user_profile_form.is_valid():
            user_profile_form.save()
            vendor.save()
            messages.success(request, 'Settings updated.')
            return redirect('vendorProfile')
        else:
            # Combine form errors to include profile picture errors
            errors = {}
            errors.update(vendor_form.errors)
            errors.update(user_profile_form.errors)
            # Include profile picture errors specifically
            errors['profile_picture'] = user_profile_form['profile_picture'].errors
            # Add error message to messages framework
            messages.error(request, 'Invalid Form.')
    else:
        vendor_form = VendorForm(instance=vendor)
        user_profile_form = UserProfileForm(instance=profile)
        errors = {}

    context = {
        'vendor_form': vendor_form,
        'profile_form': user_profile_form,
        'profile': profile,
        'vendor': vendor,
        'errors': errors,  # Include errors in context
    }
    return render(request, 'vendor/vendorProfile.html', context=context)

