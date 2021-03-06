# Generated by Django 3.2.6 on 2022-02-26 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_remove_userfavoritebook_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformations',
            name='does_lend',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userinformations',
            name='lend_in',
            field=models.DateField(blank=True, null=True),
        ),
    ]
