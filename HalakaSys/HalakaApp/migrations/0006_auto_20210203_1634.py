# Generated by Django 2.2.7 on 2021-02-03 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HalakaApp', '0005_auto_20210203_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='author',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=' المستخدم الخاص بالطالب '),
        ),
    ]
