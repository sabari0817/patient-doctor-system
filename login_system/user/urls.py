from django.urls import path
from .views import BlogPostCreateView

from .views import (
    BlogPostCreateView,
    DoctorBlogListView,
    patient_blog_list,
    signup_view,
    login_view,
    logout_view,
    patient_dashboard,
    doctor_dashboard,
    home,
)

urlpatterns = [
    # Home
    path('', home, name='home'),

    # Authentication
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Dashboards
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', doctor_dashboard, name='doctor-dashboard'),

    # Doctor Blogs
    path('doctor/blogs/new/', BlogPostCreateView.as_view(), name='doctor-blog-create'),
    path('doctor/blogs/', DoctorBlogListView.as_view(), name='doctor-blog-list'),

    # Patient Blogs
    path('blogs/', patient_blog_list, name='patient-blog-list'),
]

