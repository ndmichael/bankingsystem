from django.db import models
from django.contrib.auth.admin import User
from django.utils import timezone
from django_countries.fields import CountryField

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name="profile")
    account_number = models.CharField(max_length=10,  null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transfer_pin = models.CharField(max_length=4, null=True, blank=True)
    address = models.TextField()
    country = CountryField()
    dob = models.DateField(default=timezone.now)
    created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='avatar.png', upload_to='profile_pics/', blank=True, null=True)

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/avatar.png"

    def __str__(self):
        return f'{self.user.username}'
