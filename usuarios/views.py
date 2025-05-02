from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomRegisterForm, CustomLoginForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Cambia 'home' por tu vista principal
    else:
        form = CustomRegisterForm()
    return render(request, 'usuarios/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Cambia 'home' por tu vista principal
    else:
        form = CustomLoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def home_view(request):
    return render(request, 'usuarios/home.html', {'user': request.user})