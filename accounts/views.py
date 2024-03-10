from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
# from base64 import urlsafe_b64decode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .forms import UserForm
from vendor.forms import VendorForm
from vendor.models import Vendor
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

            # Send verification email
            mail_subject = 'Please activate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_custom_email(request, user, mail_subject, mail_template)

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

        if user_form.is_valid() and vendor_form.is_valid():
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
            mail_subject = 'Please activate your account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_custom_email(request, user, mail_subject, mail_template)
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
            return redirect('myAccount')
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


# Email verification

def activate(request, uidb64, token):
    # Now verify and activate the user using given token over email
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, User.DoesNotExist) as e:
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations. You have successfully activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid account activation.')
        return redirect('myAccount')
    

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Send reset password mail to the user
            mail_subject = 'Reset your password by clicking the link below.'
            mail_template = 'accounts/emails/reset_password_email.html'
            send_custom_email(request, user, mail_subject, mail_template)
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist.')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password changed successfully')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassowrd')
    return render(request, 'accounts/resetPassword.html')

def resetPasswordValidate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.warning(request, 'This link has been expired.')
        return redirect('login')