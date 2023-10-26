from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'accounts'

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', views.RegisterUser.as_view()),
    path('profile/', views.UserProfileRetrieveUpdateDestroy.as_view()),
    path('change_password/', views.ChangePassword.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
