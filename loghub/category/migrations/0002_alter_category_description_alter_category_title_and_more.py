# Generated by Django 5.1.3 on 2024-12-02 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="category",
            name="title",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="categorypermission",
            name="excluded_childs",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="categorypermission",
            name="included_childs",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="categorypermission",
            name="user_ids",
            field=models.JSONField(blank=True, null=True),
        ),
    ]