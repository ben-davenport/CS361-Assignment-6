from django.db import models

class Earthquake(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    magnitude = models.FloatField()
    place = models.CharField(max_length=255)
    time = models.DateTimeField()
    detail = models.URLField()
    status = models.CharField(max_length=20)
    tsunami = models.BooleanField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"Earthquake at ({self.latitude}, {self.longitude}) - Magnitude: {self.magnitude}"
