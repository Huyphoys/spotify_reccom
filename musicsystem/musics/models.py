from django.db import models

# Create your models here.
class Track(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    playlist = models.CharField(max_length=255)
    genres = models.TextField(max_length=255)
    danceability = models.FloatField()
    energy = models.FloatField()
    loudness = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.FloatField()
    key = models.FloatField()
    mode = models.FloatField()
    time_signature = models.FloatField()


    def __str__(self):
        return self.name