# Generated by Django 4.2.13 on 2024-05-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_merge_0008_merge_20240524_1101_0008_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(),
        ),
    ]
