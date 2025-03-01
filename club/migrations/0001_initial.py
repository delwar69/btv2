# Generated by Django 5.1.4 on 2025-01-15 06:27

import club.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClubMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('joining_date', models.DateField()),
                ('date_of_birth', models.DateField()),
                ('spouse_name', models.CharField(blank=True, max_length=100, null=True)),
                ('religion', models.CharField(choices=[('Islam', 'Islam'), ('Hinduism', 'Hinduism'), ('Christianity', 'Christianity'), ('Other', 'Other')], max_length=50)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=5)),
                ('permanent_address', models.TextField()),
                ('present_address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15)),
                ('phone_office', models.CharField(blank=True, max_length=15, null=True)),
                ('phone_residence', models.CharField(blank=True, max_length=15, null=True)),
                ('profile_picture', models.ImageField(default='profile_pictures/default.jpg', upload_to='profile_pictures/')),
                ('signature_image', models.ImageField(default='signature_images/default_signature.jpg', upload_to='signature_images/')),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('position', models.CharField(choices=[('President', 'President'), ('Secretary', 'Secretary'), ('Vice President', 'Vice President'), ('Joint Secretary', 'Joint Secretary'), ('Sports Secretary', 'Sports Secretary'), ('ICT Secretary', 'ICT Secretary'), ('Treasurer', 'Treasurer'), ('Finance Secretary', 'Finance Secretary'), ('Technology Secretary', 'Technology Secretary'), ('Women Affairs Secretary', 'Women Affairs Secretary'), ('Welfare Secretary', 'Welfare Secretary'), ('Executive Member', 'Executive Member')], max_length=50)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')])),
                ('image', models.ImageField(blank=True, null=True, upload_to='Committee_members/')),
                ('signature', models.ImageField(blank=True, null=True, upload_to='Committee_signatures/')),
            ],
            options={
                'ordering': ['serial_no'],
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(upload_to='gallery/')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='notices/', validators=[club.models.validate_pdf_size])),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
