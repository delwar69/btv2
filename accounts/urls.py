from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login page
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Logout page
    path('logout/', views.user_logout, name='logout'),  # Using the custom logout view
    
    # Registration page
    path('register/', views.register, name='register'),

    # User profile page
    path('profile/', views.user_profile, name='user_profile'),
    
    # User information update
    #path('update_info/', views.update_info, name='update_info'),
    path('update_info_and_full_membership/', views.update_info_and_full_membership, name='update_info_and_full_membership'),
    path('approvals/', views.approvals, name='approvals'),
    path('user_password_change/', views.user_password_change, name='user_password_change'),
    #path('user_profile/', views.user_profile, name='user_profile'),
    #forget password
    #path('password_reset/', views.password_reset_request, name='password_reset'),  # Add this line for password reset
    path('forget_password/', views.password_reset_request, name='forget_password'),  # Correct the URL here if required
    #path('password_reset/', views.password_reset_request,
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

