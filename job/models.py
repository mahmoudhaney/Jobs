from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

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