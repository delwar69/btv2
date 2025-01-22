from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now  # Import for default dates

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)  # Ensures password is hashed
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, last_name, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('focal_point', 'Focal Point'),
        ('general_secretary', 'General Secretary'),
        ('president', 'President'),
        ('superuser', 'Superuser'),
    ]
    DEPARTMENT_CHOICES = [
        ('administration', 'Administration'),
        ('finance_accounting', 'Finance & Accounting'),
        ('program', 'Program'),
        ('news', 'News'),
        ('engineering', 'Engineering'),
        ('design', 'Design'),
        ('licensing', 'Licensing'),
        ('camera', 'Camera'),
        ('information_technology', 'Information Technology (IT)'),
        ('sales', 'Sales'),
        ('security', 'Security'),
    ]    

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='member')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Information Technology (IT)')
    objects = CustomUserManager()    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


# UserProfile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email


# ClubMember Model
class ClubMember(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    
    RELIGION_CHOICES = [
        ('islam', 'Islam'),
        ('hinduism', 'Hinduism'),
        ('christianity', 'Christianity'),
        ('buddhism', 'Buddhism'),
        ('other', 'Other'),
    ]
    
    MEMBERSHIP_TYPE_CHOICES = [
        ('full', 'Full'),
        ('associate', 'Associate'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('administration', 'Administration'),
        ('finance_accounting', 'Finance & Accounting'),
        ('program', 'Program'),
        ('news', 'News'),
        ('engineering', 'Engineering'),
        ('design', 'Design'),
        ('licensing', 'Licensing'),
        ('camera', 'Camera'),
        ('information_technology', 'Information Technology (IT)'),
        ('sales', 'Sales'),
        ('security', 'Security'),
    ]
    
    # Fields from the form
    full_name = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    joining_date = models.DateField(default=now)  # Default to the current date
    #date_of_birth = models.DateField()
    date_of_birth = models.DateField(null=True, blank=True)
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    religion = models.CharField(max_length=50, choices=RELIGION_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    phone_office = models.CharField(max_length=15, blank=True, null=True)
    phone_residence = models.CharField(max_length=15, blank=True, null=True)
    permanent_address = models.TextField()
    present_address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    signature_image = models.ImageField(upload_to='signatures/', blank=True, null=True)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPE_CHOICES, default='associate')
    
    # Foreign key relationship with CustomUser model (assuming user model is used for authentication)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='club_member')
    
    # Method to return a string representation
    def __str__(self):
        return f"{self.full_name} - {self.membership_type} Member"


# Signal to create or save the profile when a CustomUser is created or updated
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        ClubMember.objects.create(user=instance, joining_date=now())  # Set joining_date to current date
    else:
        instance.userprofile.save()
