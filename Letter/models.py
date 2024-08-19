from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from filebrowser.fields import FileBrowseField
from django.conf import settings
# Create your models here.


from django.db import models
from django.conf import settings

class Letter(models.Model):
    title = models.CharField(max_length=250)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_letters', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_letters', on_delete=models.CASCADE)
    body = models.TextField()  # a TextField for rich text content
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure normal users can only send letters to admins
        if not self.sender.is_staff and not self.receiver.is_staff:
            raise ValueError("Normal users can only send letters to admins.")
        if self.sender.is_staff and self.receiver.is_staff:
            raise ValueError("Admins cannot send letters to other admins.")
        super().save(*args, **kwargs)



# class Media(models.Model):
#     MEDIA_TYPES = (
#         ('image', 'Image'),
#         ('video', 'Video'),
#         ('audio', 'Audio'),
#     )

#     letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='media')
#     media_file = FileBrowseField("File", max_length=200, directory="media/")
#     media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')

#     def __str__(self):
#         return f"{self.media_type} for post {self.post.title}"