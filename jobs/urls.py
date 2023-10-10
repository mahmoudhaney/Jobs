from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('category/', views.CategoryListCreate.as_view()),
    path('category/<int:pk>', views.CategoryRetrieveUpdateDestroy.as_view()),
    
    path('job/', views.JobListCreate.as_view()),
    path('job/<int:pk>', views.JobRetrieveUpdateDestroy.as_view()),
    
    path('candidate/', views.CandidateListCreate.as_view()),
    path('candidate/<int:pk>', views.CandidateRetrieveUpdateDestroy.as_view()),
]
