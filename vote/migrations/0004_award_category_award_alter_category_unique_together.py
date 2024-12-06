# Generated by Django 5.1.2 on 2024-12-05 08:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0003_nomination_user_preference_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='award',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vote.award'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('award', 'name')},
        ),
    ]
