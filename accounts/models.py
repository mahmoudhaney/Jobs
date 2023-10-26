from django.db import models
from django.contrib.auth.models import User
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from django.core.exceptions import ObjectDoesNotExist
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    """
    email_message = "http://127.0.0.1:8000{}?token={}".format(reverse('accounts:password_reset:reset-password-request'), reset_password_token.key)
    send_mail(
        "Account Password Reset - JobBoard",
        email_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email],
    )

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