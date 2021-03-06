# Generated by Django 2.0.3 on 2018-03-20 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hangout', '0008_auto_20180320_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hangout.Profile'),
        ),
        migrations.AlterField(
            model_name='followers',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hangout.Profile'),
        ),
    ]
