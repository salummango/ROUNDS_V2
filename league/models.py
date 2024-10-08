from django.db import models

# Create your models here.

class Fixture(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    match_date = models.DateTimeField()  # Change from DateField to DateTimeField
    round_number = models.IntegerField(default=1)
    match_stadium=models.CharField(max_length=180 )
    # match_city=models.CharField(max_length=180 )
    home_logo=models.ImageField(upload_to='calendar', default='logo2.png')
    away_logo=models.ImageField(upload_to='calendar', default='logo2.png')
    

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.match_date}"