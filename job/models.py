from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


JOB_TYPE_CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
)

def job_image_upload(instance, file_name):
    image_name, extension = file_name.split(".")
    return f"jobs/{instance.id}_{image_name}.{extension}"

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
    category = models.ForeignKey(Category, related_name='job_category', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='job_owner', on_delete=models.CASCADE)

    class Meta:
        db_table = 'job'

    def __str__(self) -> str:
        return self.title

class Candidate(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    website = models.URLField()
    cv = models.FileField(upload_to='candidatesCVs/')
    cover_letter = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    job = models.ForeignKey(Job, related_name='apply_job', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

@receiver(pre_save, sender=Candidate)
def pre_save_cv(sender, instance, *args, **kwargs):
    """ Delete old candidate CV if new one is uploaded """
    old_image = instance.__class__.objects.get(id=instance.id).cv
    if instance.cv != old_image:
        old_image.delete(save=False)

@receiver(post_delete, sender=Candidate)
def post_delete_cv(sender, instance, *args, **kwargs):
    """ Delete candidate's CV when delete him """
    try:
        instance.cv.delete(save=False)
    except:
        pass