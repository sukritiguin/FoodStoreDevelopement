from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from .utils import *

# Retricting the vendor from accessing to the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Retricting the customer from accessing to the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are a registered user.')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # - Create the user using the form data
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = 2
            # user.save()

            # - Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully.')
            return redirect('registerUser')
        else: # - If form is not valid
            # print("Invalid form....")
            # print(form.errors)
            pass
    else:
        form = UserForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context=context)



def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are a registered user.')
        return redirect('myAccount')
    elif request.method == 'POST':
        user_form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)

        print("================================================================")
        print("CAME HERE>>>>>")
        print("================================================================")

        if(user_form.is_valid()):
            print("================================================")
            print("User form is valid")
            print("================================================")
        
        if(vendor_form.is_valid()):
            print("================================================")
            print("Vendor form is valid")
            print("================================================")

        if user_form.is_valid() and vendor_form.is_valid():
            print("================================================================")
            print("Both form is valid")
            print("================================================================")
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user = user) # Generating from signal : getting data from django signal
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your register has been registered successfully. Wait for the approval.')
            return redirect('registerVendor')
        else:
            print("Invalid form")
            print(user_form.errors)
            print(vendor_form.errors)
    else:
        user_form = UserForm()
        vendor_form = VendorForm()

    context = {
        'form': user_form,
        'vendor_form': vendor_form,
    }

    return render(request, 'accounts/registerVendor.html', context=context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credential.')
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required
def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    auth.logout(request)
    messages.info(request, 'You are now logged out.')
    return redirect('login')

# @login_required
# def dashboard(request):
#     return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectURL = detectUser(user)

    return redirect(redirectURL)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

