# Generated by Django 3.2.5 on 2021-09-04 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_custmor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='custmor',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]