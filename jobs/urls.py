from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('category/', views.CategoryListCreate.as_view()),
    path('category/<int:pk>', views.CategoryRetrieveUpdateDestroy.as_view()),
    path('category/<int:pk>/jobs', views.ListCategoryJobs.as_view()),
    
    path('job/', views.JobListCreate.as_view()),
    path('job/<int:pk>', views.JobRetrieveUpdateDestroy.as_view()),
    path('job/<int:pk>/applications', views.ListJobApplications.as_view()),
    path('job/applications/<int:pk>', views.RetrieveJobApplication.as_view()),
    # path('job/<int:pk>/applications/<int:id>', views.ListJobApplications.as_view()), This is the most right one
    
    path('application/', views.ApplicationListCreate.as_view()),
    path('application/<int:job_id>', views.ApplicationRetrieveUpdateDestroy.as_view()),
]
