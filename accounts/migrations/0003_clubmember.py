# Generated by Django 5.1.4 on 2025-01-20 16:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('designation', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('joining_date', models.DateField()),
                ('date_of_birth', models.DateField()),
                ('spouse_name', models.CharField(blank=True, max_length=100, null=True)),
                ('religion', models.CharField(choices=[('islam', 'Islam'), ('hinduism', 'Hinduism'), ('christianity', 'Christianity'), ('buddhism', 'Buddhism'), ('other', 'Other')], max_length=50)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('phone_office', models.CharField(blank=True, max_length=15, null=True)),
                ('phone_residence', models.CharField(blank=True, max_length=15, null=True)),
                ('permanent_address', models.TextField()),
                ('present_address', models.TextField()),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('signature_image', models.ImageField(blank=True, null=True, upload_to='signatures/')),
                ('membership_type', models.CharField(choices=[('full', 'Full'), ('associate', 'Associate')], default='associate', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='club_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
