# Generated by Django 3.2.6 on 2022-02-19 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_userinformations_subscription_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformations',
            name='subscription_type',
            field=models.CharField(blank=True, choices=[('برنزی (یک ماهه)', 'bronze(1 months)'), ('نقره\u200cای (سه ماهه)', 'silver(3 months)'), ('طلایی (یک ساله)', 'golden(12 months)')], max_length=20, null=True),
        ),
    ]