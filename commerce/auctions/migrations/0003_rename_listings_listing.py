# Generated by Django 4.0.6 on 2022-12-01 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Listings',
            new_name='Listing',
        ),
    ]