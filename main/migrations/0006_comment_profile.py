# Generated by Django 5.1.4 on 2025-05-12 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userprofile'),
        ),
    ]
