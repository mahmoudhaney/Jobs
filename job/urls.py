from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('', views.jobs, name='jobs'),
    # path('dashboard', views.dashboard, name='job_dashboard'),
    path('<int:id>', views.job_details, name='job_details'),
    path('add', views.add_job, name='add_jobs'),
    path('<int:id>/edit', views.edit_job, name='edit_job'),
    path('<int:id>/delete', views.delete_job, name='delete_job'),
    path('<int:id>/apply', views.job_apply, name='job_apply'),
]
