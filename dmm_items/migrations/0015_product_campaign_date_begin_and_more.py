# Generated by Django 5.2.3 on 2025-07-04 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmm_items', '0014_remove_product_genres_product_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='campaign_date_begin',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='campaign_date_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
