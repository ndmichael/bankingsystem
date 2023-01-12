from django.db import models
from django.contrib.auth.admin import User
from django.utils import timezone
from django_countries.fields import CountryField

# Create your models here.

class Client(models.Model):
    gender = (
        ('male', 'MALE'),
        ('female', 'FEMALE')
    )
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name="profile")
    account_number = models.CharField(max_length=20,  null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transfer_pin = models.CharField(max_length=4, null=True, blank=True)
    address = models.TextField()
    country = CountryField()
    dob = models.DateField(default=timezone.now)
    gender= models.CharField(max_length=7, choices=gender, default="male")
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


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transfer")
    currency = models.CharField(max_length=10, default="US DOLLAR")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    IBAN = models.CharField(max_length = 34, blank=True, null=True)
    receivers_name = models.CharField(max_length=50)
    beneficiary_account_number = models.CharField(max_length=20)
    beneficiary_bank_address = models.TextField()
    country = CountryField()
    dotf = models.DateTimeField(default=timezone.now)
    is_success =  models.BooleanField(default=False)

    def __str__(self):
        return f'{self.receivers_name}'