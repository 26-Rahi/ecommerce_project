# Generated by Django 5.2 on 2025-05-09 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_orderiem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderIem',
            new_name='OrderItem',
        ),
    ]
