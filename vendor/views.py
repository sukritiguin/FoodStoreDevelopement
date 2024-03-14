from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.http import JsonResponse

from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from menu.models import Category, FoodItem
from menu.forms import CategoryForm
from accounts.views import check_role_vendor
from .models import Vendor

# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

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

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorMenuBuilder(request):
    vendor = get_vendor(request)
    # categories = Category.objects.filter(vendor=vendor)
    sort_by = request.GET.get('sort', None)
    if sort_by == 'category_name':
        categories = Category.objects.filter(vendor=vendor).order_by('category_name')
    elif sort_by == 'created_at':
        categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    elif sort_by == 'updated_at':
        categories = Category.objects.filter(vendor=vendor).order_by('-updated_at')
    else:
        categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/vendorMenuBuilder.html', context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorMenuBuilderCategory(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    foodItems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'category': category,
        'foodItems': foodItems,
    }
    return render(request, 'vendor/vendorMenuBuilderCategory.html', context=context)

def vendorMenuBuilderAddCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('vendorMenuBuilder')
        else:
            pass
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/vendorMenuBuilderAddCategory.html', context=context)

def vendorMenuBuilderEditCategory(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request=request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('vendorMenuBuilder')
        else:
            pass
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/vendorMenuBuilderEditCategory.html', context=context)


def vendorMenuBuilderDeleteCategory(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully.')
    return redirect('vendorMenuBuilder')

