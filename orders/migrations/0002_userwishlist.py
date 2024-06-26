# Generated by Django 4.2.2 on 2023-07-05 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0007_brands_is_active_categories_is_active_and_more'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.productvariants')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
