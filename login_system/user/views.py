from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils.text import Truncator

from .forms import SignupForm, BlogPostForm
from .models import CustomUser, BlogPost

# -----------------------------
# Mixin to restrict doctor views
# -----------------------------
class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'doctor'

# -----------------------------
# Doctor Views
# -----------------------------
class BlogPostCreateView(LoginRequiredMixin, DoctorRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'user/blogpost_form.html'
    success_url = reverse_lazy('doctor-blog-list')

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        return super().form_valid(form)

class DoctorBlogListView(LoginRequiredMixin, DoctorRequiredMixin, ListView):
    model = BlogPost
    template_name = 'user/doctor_blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return BlogPost.objects.filter(doctor=self.request.user)

# -----------------------------
# Patient Views
# -----------------------------
@login_required
def patient_blog_list(request):
    category = request.GET.get('category')

    if category:
        blogs = BlogPost.objects.filter(status='Published', category=category)
    else:
        blogs = BlogPost.objects.filter(status='Published')

    # Truncate summary to 15 words
    for blog in blogs:
        blog.truncated_summary = Truncator(blog.summary).words(15, truncate='...')

    # Get unique categories for filtering
    categories = BlogPost.objects.values_list('category', flat=True).distinct()

    context = {
        'blogs': blogs,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'user/patient_blog_list.html', context)

# -----------------------------
# Authentication Views
# -----------------------------
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == 'patient':
                return redirect('patient_dashboard')
            elif user.role == 'doctor':
                return redirect('doctor-dashboard')
        else:
            error = "Invalid username or password"
    return render(request, 'user/login.html', {"error": error})

def logout_view(request):
    logout(request)
    return redirect('login')

# -----------------------------
# Dashboard / Home Views
# -----------------------------
@login_required
def patient_dashboard(request):
    return render(request, 'user/patient_dashboard.html', {'user': request.user})

@login_required
def doctor_dashboard(request):
    return render(request, 'user/doctor_dashboard.html', {'user': request.user})

def home(request):
    return render(request, 'user/home.html')
