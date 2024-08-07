from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm
from django.contrib.auth import login as auth_login


def home_view(request):
    return render(request, "home.html")


def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register.html', {'form': form})
