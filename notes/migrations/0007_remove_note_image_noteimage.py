# Generated by Django 5.2.2 on 2025-06-11 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_add_school_subjects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='image',
        ),
        migrations.CreateModel(
            name='NoteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='notes/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='notes.note')),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
    ]
