
from django.db import models
from pytz import timezone
from django.utils import timezone 

class Prediction(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    image = models.ImageField(upload_to='predictions/')
    predicted_disease = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)

    date = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name