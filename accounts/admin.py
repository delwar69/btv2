from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, ClubMember  # Import ClubMember model

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name','department', 'role', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Basic authentication fields
        ('Personal Info', {'fields': ('first_name', 'last_name', 'department', 'role')}),  # Personal info fields
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),  # Permission-related fields
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'role')
    ordering = ('email',)

# Register CustomUser with its admin class
admin.site.register(CustomUser, CustomUserAdmin)

# Register UserProfile for managing profiles in the admin panel
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture')  # Added 'profile_picture' to display
    search_fields = ('user__email',)

# Register ClubMember for managing club members in the admin panel
@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'designation', 'department', 'membership_type', 'email', 'phone_number','permanent_address', 'joining_date')
    list_filter = ('membership_type', 'department', 'gender', 'blood_group', 'religion')
    search_fields = ('full_name', 'email', 'department', 'role')
    ordering = ('full_name',)

