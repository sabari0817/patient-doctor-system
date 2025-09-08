from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser
from django.contrib import admin
from .models import Category, BlogPost




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "doctor", "category", "created_at")  # use 'doctor'
    list_filter = ("category", "created_at")
    search_fields = ("title", "content")


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'username',
        'email',
        'role',
        'city',
        'state',
        'pincode',
        'profile_pic_preview',
        'is_staff',
        'is_active',
    ]

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'profile_pic', 'address1', 'city', 'state', 'pincode')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'profile_pic', 'address1', 'city', 'state', 'pincode')}),
    )

    # Show profile picture preview in list view
    def profile_pic_preview(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_pic.url)
        return "No Image"

    profile_pic_preview.short_description = "Profile Picture"


admin.site.register(CustomUser, CustomUserAdmin)
