# Generated by Django 4.0.5 on 2022-06-01 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='birth_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Date of birth'),
        ),
    ]
