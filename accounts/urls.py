from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('get-details', views.UserRetrieveAPI.as_view()),
    path('register', views.RegisterUserAPIView.as_view()),
]
