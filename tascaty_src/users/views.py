from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserLoginForm
from django.contrib.auth.forms import PasswordChangeForm


def Login(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        django_login(request, user)
        if next:
            return redirect(next)
        return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            messages.success(
                request, f'You Password has been updated successfully, please login now  !!')
            return redirect('login')
    context = {
        'title': 'TasCaty|Password Change'
        }
    return render(request, 'users/password_change.html', context)


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'Tascaty|User Profile'})
