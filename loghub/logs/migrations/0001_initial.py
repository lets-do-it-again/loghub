# Generated by Django 5.1.3 on 2024-11-19 18:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
                ('log_key', models.SlugField(unique=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField()),
                ('is_public', models.BooleanField(default=True)),
                ('deleted_at', models.DateTimeField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='category.categorydetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SourceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('is_digital', models.BooleanField()),
                ('text', models.TextField()),
                ('meta_data', models.JSONField()),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='logs.log')),
            ],
        ),
    ]