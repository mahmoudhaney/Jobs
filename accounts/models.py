from django.db import models
from django.contrib.auth.models import User
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from django.core.exceptions import ObjectDoesNotExist

def user_image_upload(instance, file_name):
    image_name, extension = file_name.split(".")
    return f"profiles/{str(uuid.uuid4())}.{extension}"

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default='Egypt')
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to=user_image_upload, default=None)

    def __str__(self) -> str:
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Once a new user is created, create a profile for him """
    if created:
        Profile.objects.create(user=instance)

@receiver(pre_save, sender=Profile)
def pre_save_img(sender, instance, *args, **kwargs):
    """ Delete old User's image if new one is uploaded """
    try:
        if instance.__class__.objects.get(id=instance.id).image:
            old_image = instance.__class__.objects.get(id=instance.id).image
            if instance.image != old_image:
                old_image.delete(save=False)
    except ObjectDoesNotExist:
        pass

@receiver(post_delete, sender=Profile)
def post_delete_img(sender, instance, *args, **kwargs):
    """ Delete Users's image when delete it """
    try:
        instance.image.delete(save=False)
    except:
        pass