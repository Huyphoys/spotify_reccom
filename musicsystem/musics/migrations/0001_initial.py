# Generated by Django 4.2.7 on 2023-11-28 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('artist_id', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('playlist_id', models.CharField(max_length=255)),
                ('playlist', models.CharField(max_length=255)),
                ('genres', models.TextField(max_length=255)),
                ('danceability', models.FloatField()),
                ('energy', models.FloatField()),
                ('loudness', models.FloatField()),
                ('speechiness', models.FloatField()),
                ('acousticness', models.FloatField()),
                ('instrumentalness', models.FloatField()),
                ('liveness', models.FloatField()),
                ('valence', models.FloatField()),
                ('tempo', models.FloatField()),
                ('duration_ms', models.FloatField()),
                ('key', models.FloatField()),
                ('mode', models.FloatField()),
                ('time_signature', models.FloatField()),
            ],
        ),
    ]
