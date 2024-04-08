from django.db import models
import json

# Create your models here.

class Rule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.JSONField()
   

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure value is stored as JSON
        if isinstance(self.value, dict) or isinstance(self.value, list):
            self.value = json.dumps(self.value)
        super().save(*args, **kwargs)