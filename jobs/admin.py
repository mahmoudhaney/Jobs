from django.contrib import admin
from .models import Category, Job, Candidate

admin.site.register(Category)
admin.site.register(Job)
admin.site.register(Candidate)
