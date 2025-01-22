import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, CustomAuthenticationForm, UserProfileForm
from .models import CustomUser, UserProfile
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import ClubMemberForm
from .models import ClubMember
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile
from django.shortcuts import render, get_object_or_404



# This method will handle form submission and generate a PDF upon successful submission
def update_info_and_full_membership(request):
    if request.method == 'POST':
        form = ClubMemberForm(request.POST, request.FILES)
        if form.is_valid():
            club_member = form.save()
            
            # Generate the PDF
            #pdf_response = generate_member_pdf(club_member)
            #return pdf_response
        else:
            # Display the form with errors
            return render(request, 'accounts/update_info_and_full_membership.html', {'form': form})
    else:
        form = ClubMemberForm()
    return render(request, 'accounts/update_info_and_full_membership.html', {'form': form})



def update_info_and_full_membership(request):
    user = request.user  # Assuming the user is logged in
    club_member = get_object_or_404(ClubMember, user=user)

    if request.method == 'POST':
        form = ClubMemberForm(request.POST, request.FILES, instance=club_member)
        if form.is_valid():
            form.save()
            # Redirect or show success message
    else:
        form = ClubMemberForm(instance=club_member)

    return render(request, 'update_info_and_full_membership.html', {'form': form})




def generate_member_pdf(club_member):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Add content to the PDF
    p.drawString(100, 750, f"Membership Information for {club_member.first_name} {club_member.last_name}")
    p.drawString(100, 730, f"Email: {club_member.email}")
    p.drawString(100, 710, f"Phone: {club_member.phone_number}")
    p.drawString(100, 690, f"Address: {club_member.address}")
    p.drawString(100, 670, f"Membership Type: {club_member.membership_type}")

    # You can also include images like the profile picture or signature in the PDF if needed
    if club_member.profile_picture:
        p.drawImage(club_member.profile_picture.path, 100, 550, width=100, height=100)

    # Finalize the PDF
    p.showPage()
    p.save()
    
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{club_member.first_name}_{club_member.last_name}_membership.pdf"'
    return response


def update_info(request):
    return render(request, 'accounts/update_info.html')

def approvals(request):
    return render(request, 'accounts/approvals.html')

#user password change form
@login_required
def user_password_change(request):
    """Handles user password change."""
    if request.method == 'POST':
        # Create a PasswordChangeForm with the logged-in user
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            # Save the new password
            form.save()
            # Update the session to keep the user logged in
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been successfully changed.")
            return redirect('user_profile')  # Redirect to profile page after successful change
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/user_password_change.html', {'form': form})

# Setting up logger for error handling
logger = logging.getLogger(__name__)

@login_required
def user_logout(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def register(request):
    """Handles user registration."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the user instance without committing to DB
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()  # Save the user to the database (triggers the signal to create UserProfile)

            # Generate email activation link
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            activation_link = f"http://{get_current_site(request).domain}/accounts/activate/{uid}/{token}/"

            # Send activation email with error handling
            try:
                send_mail(
                    "Activate your account",
                    f"Click here to activate your account: {activation_link}",
                    'doictsadarbrahmanbarian@gmail.com',  # Sender email
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, "Please check your email to verify your account.")
            except Exception as e:
                logger.error(f"Failed to send activation email: {e}")
                messages.error(request, "An error occurred while sending the activation email. Please try again.")
                return redirect('register')  # Redirect to registration page on failure

            return redirect('login')  # Redirect to login page on success
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def activate(request, uidb64, token):
    """Handles account activation."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully!")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect('login')

def user_login(request):
    """Handles user login."""
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' refers to the email field
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)  # Use `username=email`
            if user is not None:
                login(request, user)
                return redirect('user_profile')  # Redirect to profile or dashboard
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_profile(request):
    """Handles user profile viewing and editing."""
    user = request.user  # Get the logged-in user
    # Get or create the UserProfile for the logged-in user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        # Initialize the form with POST data, FILES, and the associated user profile instance
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Save the updated profile
            messages.success(request, "Your profile has been successfully updated.")
            return redirect('user_profile')  # Redirect to the same page after saving
        else:
            messages.error(request, "Failed to update your profile. Please check the form for errors.")
    else:
        # Prepopulate the form with the current profile data
        form = UserProfileForm(instance=profile)
    # Render the profile page with the form and profile details
    return render(request, 'accounts/user_profile.html', {'form': form, 'profile': profile})


def password_reset_request(request):
    """Handles sending a password reset link."""
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.txt"
                    context = {
                        "email": user.email,
                        "domain": get_current_site(request).domain,
                        "site_name": "BTV Officers Club",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email_content = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, email_content, 'doictsadarbrahmanbarian@gmail.com', [user.email], fail_silently=False)
                    except Exception as e:
                        logger.error(f"Failed to send password reset email to {user.email}: {e}")
                        messages.error(request, "Error sending password reset email. Try again later.")
                        return redirect('password_reset')
                messages.success(request, "A password reset link has been sent to your email.")
                return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/forget_password.html', {'form': form})
