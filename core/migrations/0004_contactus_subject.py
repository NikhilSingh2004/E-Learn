# Generated by Django 5.0.2 on 2024-03-09 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_comment_parent_alter_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='subject',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
