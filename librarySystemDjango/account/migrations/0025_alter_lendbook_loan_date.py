# Generated by Django 4.0.3 on 2022-03-29 07:08

import datetime
from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_alter_lendbook_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lendbook',
            name='loan_date',
            field=django_jalali.db.models.jDateField(default=datetime.date(2022, 3, 29)),
        ),
    ]