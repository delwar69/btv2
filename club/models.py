from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Custom validator for file size
def validate_pdf_size(value):
    if value.size > 5 * 1024 * 1024:  # 5 MB limit
        raise ValidationError("The PDF file size must not exceed 5 MB.")

# Notice model for storing club notices
class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='notices/', blank=True, null=True, validators=[validate_pdf_size])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# GalleryImage model for storing images in the gallery
class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.title

# Member model for storing information about committee members
class CommitteeMember(models.Model):
    POSITION_CHOICES = [
        ('President', 'President'),
        ('Secretary', 'Secretary'),
        ('Vice President', 'Vice President'),
        ('Joint Secretary', 'Joint Secretary'),
        ('Sports Secretary', 'Sports Secretary'),
        ('ICT Secretary', 'ICT Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Finance Secretary', 'Finance Secretary'),
        ('Technology Secretary', 'Technology Secretary'),
        ('Women Affairs Secretary', 'Women Affairs Secretary'),
        ('Welfare Secretary', 'Welfare Secretary'),
        ('Executive Member', 'Executive Member'),
    ]

    serial_no = models.PositiveIntegerField(unique=True)  # Updated to match admin.py
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    email = models.EmailField(max_length=255, blank=True, null=True)
    mobile = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
    )
    image = models.ImageField(upload_to='Committee_members/', blank=True, null=True)
    signature = models.ImageField(upload_to='Committee_signatures/', blank=True, null=True)

    class Meta:
        ordering = ['serial_no']  # Ensure it matches admin.py

    def __str__(self):
        return f"{self.position}: {self.name}"

# ClubMember model for new member registrations
class ClubMember(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    RELIGION_CHOICES = [
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('Christianity', 'Christianity'),
        ('Other', 'Other'),
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

    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()
    date_of_birth = models.DateField()
    spouse_name = models.CharField(max_length=100, blank=True, null=True)
    religion = models.CharField(max_length=50, choices=RELIGION_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    permanent_address = models.TextField()
    present_address = models.TextField()
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    phone_office = models.CharField(max_length=15, blank=True, null=True)
    phone_residence = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=False,
        null=False,
        default='profile_pictures/default.jpg',
    )
    signature_image = models.ImageField(
        upload_to='signature_images/',
        blank=False,
        null=False,
        default='signature_images/default_signature.jpg',
    )

    def __str__(self):
        return self.name
