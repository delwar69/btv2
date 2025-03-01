from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from .models import CustomUser, UserProfile, ClubMember
from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class ClubMemberForm(forms.ModelForm):
    same_as_permanent = forms.BooleanField(required=False, label="Same as Permanent Address")

    class Meta:
        model = ClubMember
        fields = '__all__'  # Includes email and other fields
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'spouse_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter spouse name'}),
            'religion': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter permanent address'}),
            'present_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter present address'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
                'readonly': 'readonly',  # Prevent editing
            }),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'phone_office': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter office phone number'}),
            'phone_residence': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter residence phone number'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'signature_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        permanent_address = cleaned_data.get('permanent_address')
        same_as_permanent = cleaned_data.get('same_as_permanent')
        present_address = cleaned_data.get('present_address')

        if same_as_permanent:  # If checkbox is checked, copy permanent address to present address
            if not present_address:
                cleaned_data['present_address'] = permanent_address
        return cleaned_data

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        joining_date = self.cleaned_data.get('joining_date')

        if date_of_birth is None:
            raise forms.ValidationError("Date of Birth is required.")

        if joining_date and (joining_date - date_of_birth).days < 18 * 365:
            raise forms.ValidationError("Date of Birth must be at least 18 years before the Joining Date.")

        return date_of_birth

    def clean_joining_date(self):
        joining_date = self.cleaned_data.get('joining_date')
        if joining_date is None:
            raise forms.ValidationError("Joining Date is required.")

        if joining_date > now().date():
            raise forms.ValidationError("Joining Date cannot be in the future.")
        
        return joining_date

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            try:
                image = Image.open(profile_picture)
                if image.size != (300, 300):
                    raise forms.ValidationError("Profile picture should be 300x300 pixels.")
            except FileNotFoundError:
                raise forms.ValidationError("The uploaded file could not be opened.")
        return profile_picture

    def clean_signature_image(self):
        signature_image = self.cleaned_data.get('signature_image')
        if signature_image:
            try:
                image = Image.open(signature_image)
                if image.size != (300, 80):  # Validate the size
                    raise forms.ValidationError("Signature image should be 300x80 pixels.")
            except Exception as e:
                raise forms.ValidationError(f"Error opening signature image: {e}")
        return signature_image

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label="Password",
        validators=[
            MinLengthValidator(8, "Password must be at least 8 characters."),
            RegexValidator(r'[A-Z]', "Password must contain at least one uppercase letter."),
            RegexValidator(r'[0-9]', "Password must contain at least one digit."),
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        }),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label="Password"
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture',
            'bio',
            'date_of_birth',
            'gender',
            'phone_number',
            'permanent_address',
            'current_address',
        ]
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write something about yourself...'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'gender': forms.Select(choices=[
                ('male', 'Male'),
                ('female', 'Female'),
                ('other', 'Other'),
            ], attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'permanent_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your permanent address',
                'rows': 2,
            }),
            'current_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your current address',
                'rows': 2,
            }),
        }