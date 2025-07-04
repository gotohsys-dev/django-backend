# Generated by Django 5.2.3 on 2025-06-20 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmm_items', '0003_alter_product_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url_list',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url_large',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_url_small',
            field=models.URLField(blank=True, null=True),
        ),
    ]
