# Generated by Django 5.1.4 on 2025-01-19 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('courses', models.ManyToManyField(null=True, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uni_name', models.CharField(max_length=100)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('professors', models.ManyToManyField(related_name='professors', to='uni_prof.professor')),
            ],
        ),
        migrations.AddField(
            model_name='professor',
            name='universities',
            field=models.ManyToManyField(to='uni_prof.university'),
        ),
    ]
