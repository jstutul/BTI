from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, Institution, Student


# ✅ Step 1: Create Profile automatically
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        role=""
        if instance.is_superuser:
            role = 'admin'
        elif instance.is_staff:
            role = 'institution'
        else:
            role = 'student'

        Profile.objects.create(
                user=instance,
                role=role
            )
       
        