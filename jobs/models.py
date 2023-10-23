from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import uuid
from django.core.exceptions import ObjectDoesNotExist

# Category
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

# Job
JOB_TYPE_CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
)

def job_image_upload(instance, file_name):
    image_name, extension = file_name.split(".")
    return f"jobs/{str(uuid.uuid4())}.{extension}"

class Job(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=2000)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    vacancy = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    salary = models.PositiveIntegerField(default=100, validators=[MinValueValidator(100), MaxValueValidator(100000)]) 
    experience = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    location = models.CharField(max_length=100, default='Egypt')
    image = models.FileField(upload_to=job_image_upload, default='none')
    published_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='jobs', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='job_owner', on_delete=models.CASCADE)

    class Meta:
        db_table = 'job'

    def __str__(self) -> str:
        return self.title

@receiver(pre_save, sender=Job)
def pre_save_img(sender, instance, *args, **kwargs):
    """ Delete old job's image if new one is uploaded """
    try:
        if instance.__class__.objects.get(id=instance.id).image:
            old_image = instance.__class__.objects.get(id=instance.id).image
            if instance.image != old_image:
                old_image.delete(save=False)
    except ObjectDoesNotExist:
        pass

@receiver(post_delete, sender=Job)
def post_delete_img(sender, instance, *args, **kwargs):
    """ Delete job's image when delete it """
    try:
        instance.image.delete(save=False)
    except:
        pass

# Application
def application_cv_upload(instance, file_name):
    cv_name, extension = file_name.split(".")
    return f"applicationCVs/{str(uuid.uuid4())}.{extension}"

class Application(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    website = models.URLField()
    cv = models.FileField(upload_to=application_cv_upload, default='none')
    cover_letter = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='applicatoin_owner', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('job', 'owner')

    def __str__(self) -> str:
        return self.name

@receiver(pre_save, sender=Application)
def pre_save_cv(sender, instance, *args, **kwargs):
    """ Delete old Application CV if new one is uploaded """
    try:
        if instance.__class__.objects.get(id=instance.id).cv:
            old_cv = instance.__class__.objects.get(id=instance.id).cv
            if instance.cv != old_cv:
                old_cv.delete(save=False)
    except ObjectDoesNotExist:
        pass

@receiver(post_delete, sender=Application)
def post_delete_cv(sender, instance, *args, **kwargs):
    """ Delete Application's CV when delete it """
    try:
        instance.cv.delete(save=False)
    except:
        pass
