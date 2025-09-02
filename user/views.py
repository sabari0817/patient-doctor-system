from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import CustomUser



def home(request):
    return render(request, 'user/home.html')

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Trying to login with:", username, password)  # debug

        user = authenticate(request, username=username, password=password)
        print("Auth result:", user)  # debug

        if user:
            login(request, user)
            if user.role == 'patient':
                return redirect('patient_dashboard')
            elif user.role == 'doctor':
                return redirect('doctor_dashboard')
        else:
            error = "Invalid username or password"
    return render(request, 'user/login.html', {"error": error})

@login_required
def patient_dashboard(request):
    return render(request, 'user/patient_dashboard.html', {'user': request.user})

@login_required
def doctor_dashboard(request):
    return render(request, 'user/doctor_dashboard.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')
