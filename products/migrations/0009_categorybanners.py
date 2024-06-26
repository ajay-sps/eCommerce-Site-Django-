# Generated by Django 4.2.2 on 2023-07-28 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_properties_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryBanners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='products/category_banner')),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='products.categories')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
