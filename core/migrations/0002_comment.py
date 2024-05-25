# Generated by Django 5.0.2 on 2024-02-29 14:35

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.topic')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.comment')),
            ],
        ),
    ]