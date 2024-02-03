from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import User
import uuid


@receiver(pre_save, sender=User)
def generate_userID(sender, instance, **kwargs):
    if instance.id == '':
        instance.id = str(uuid.uuid4()).replace('-', '')[:30]

    try:
        # Calculate a user's age
        if not instance.is_superuser:
            if timezone.now().strftime('%Y-%m-%d %H:%M:%S') > instance.date_joined.strftime('%Y-%m-%d %H:%M:%S'):
                user_dob = instance.dob
                current_date = timezone.now().date()
                age = current_date - user_dob
                instance.age = int(age.days/365.25)
                
            else:
                user_dob = instance.dob
                current_date = timezone.now().date()
                age = current_date - user_dob
                instance.age = int(age.days/365.25)
    
    except AttributeError:
        return
