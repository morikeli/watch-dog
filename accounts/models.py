from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ User model used in this project. """
    
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    email = models.EmailField(unique=True, blank=False)
    gender = models.CharField(max_length=7, blank=False)
    mobile_no = PhoneNumberField(blank=False, db_column='Mobile No.')
    dob = models.DateField(null=True, blank=False, db_column='DoB')
    age = models.PositiveIntegerField(default=0, editable=False)
    national_id = models.PositiveBigIntegerField(max_length=8, blank=False, db_column='ID no.')
    county = models.CharField(max_length=30, blank=False)
    sub_county = models.CharField(max_length=30, blank=False)
    profile_pic = models.ImageField(upload_to='Users/imgs/dps/', default='default.png')
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username