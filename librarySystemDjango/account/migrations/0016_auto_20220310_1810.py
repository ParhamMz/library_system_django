# Generated by Django 3.2.6 on 2022-03-10 14:40

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_alter_userinformations_test_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformations',
            name='test_date',
        ),
        migrations.AlterField(
            model_name='userinformations',
            name='birth_date',
            field=django_jalali.db.models.jDateField(),
        ),
        migrations.AlterField(
            model_name='userinformations',
            name='end_subs',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userinformations',
            name='lend_in',
            field=django_jalali.db.models.jDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userinformations',
            name='start_subs',
            field=django_jalali.db.models.jDateTimeField(blank=True, null=True),
        ),
    ]
