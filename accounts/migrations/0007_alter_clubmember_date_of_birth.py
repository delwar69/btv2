# Generated by Django 5.1.4 on 2025-01-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customuser_department_alter_clubmember_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubmember',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
