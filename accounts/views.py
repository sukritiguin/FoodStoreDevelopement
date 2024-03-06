from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import UserForm
from .models import User

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
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
            user.role = 2
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