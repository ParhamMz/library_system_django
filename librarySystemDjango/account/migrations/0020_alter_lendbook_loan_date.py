# Generated by Django 3.2.6 on 2022-03-26 13:36

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_lendbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lendbook',
            name='loan_date',
            field=django_jalali.db.models.jDateField(auto_now_add=True),
        ),
    ]
