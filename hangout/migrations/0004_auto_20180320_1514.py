# Generated by Django 2.0.3 on 2018-03-20 15:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hangout', '0003_auto_20180319_1621'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Favorite',
            new_name='FavoritePost',
        ),
    ]
