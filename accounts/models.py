from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class User(AbstractUser):
    """ User model used in this project. """
    
    id = models.CharField(max_length=30, primary_key=True, unique=True, editable=False)
    email = models.EmailField(unique=True, blank=False)
    gender = models.CharField(max_length=7, blank=False)
    mobile_no = PhoneNumberField(blank=False, db_column='Mobile No.')
    dob = models.DateField(null=True, blank=False, db_column='DoB')
    age = models.PositiveIntegerField(default=0, editable=False)
    national_id = models.PositiveBigIntegerField(blank=False, default=0,db_column='ID no.')
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


    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if (img.height >= 480 and img.width > 480) or (img.height >= 480 or img.width >= 480):
            output_size = (320, 320)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)


    def delete(self, *args, **kwargs):
        self.profile_pic.delete()
        super(User, self).delete(*args, **kwargs)
