# Generated by Django 5.1.4 on 2025-02-01 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_alter_course_avg_cognitive_load_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='has_reviews',
        ),
    ]
