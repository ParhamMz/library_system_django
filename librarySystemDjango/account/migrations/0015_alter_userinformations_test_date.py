# Generated by Django 3.2.6 on 2022-03-10 14:31

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_userinformations_test_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformations',
            name='test_date',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True),
        ),
    ]
