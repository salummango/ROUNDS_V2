from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Team(models.Model):
    TeamName = models.CharField(max_length=255)
    TeamStadium = models.CharField(max_length=255)
    TeamCity = models.CharField(max_length=255)

    def __str__(self):
        return self.TeamName


# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.pop('team', None)  # Remove 'team' field from extra_fields
        
        return self._create_user(email=email, password=password, first_name=first_name, last_name=last_name, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        if not password:
            raise ValueError("The Password field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phoneNo = models.IntegerField()
    userImage = models.ImageField(upload_to='userimage')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phoneNo']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


