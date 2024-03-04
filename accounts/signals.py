from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_reciver(sender, instance, created, **kwargs):
    if created: # when user is created -> then -> UserProfile will also create
        UserProfile.objects.create(user=instance)
    else: # when user is updated -> UserProfile will also update
        try: # when userProfile is exists and we are trying to update that userProfile
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except: # when userProfile is not exists and we are trying to update that userProfile
            # So we need to create userProfile now
            UserProfile.objects.create(user=instance)