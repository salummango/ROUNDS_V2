from django.db import models

# Create your models here.

class HistoricalFixtureFile(models.Model):
    file = models.FileField(upload_to='historical_fixtures/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded at {self.uploaded_at}"

