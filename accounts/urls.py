from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', views.RegisterUser.as_view()),
    path('profile/', views.UserProfileRetrieveUpdateDestroy.as_view()),
]
