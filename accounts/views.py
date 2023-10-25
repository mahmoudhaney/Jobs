from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework import status

class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Override Post Function Reasons:
        1- To create a token for user once he registered
        2- To respond with it's token istead of login 
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class UserProfileRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Override 'get', 'put', and 'delete' functions
    to user token auth instead of 'pk' in url
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            user = self.model.objects.get(id=request.user.id)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except self.model.DoesNotExist:
            return Response({'detail': "Not found."}, status= status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        try:
            user = self.model.objects.get(id=request.user.id)
            serializer = self.get_serializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
            return Response({'detail': "Not found."}, status= status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            user.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'detail': "Not found."}, status= status.HTTP_404_NOT_FOUND)

class ChangePassword(generics.UpdateAPIView):
    """
    Change User Password
    """
    model = User
    serializer_class = ChangePasswordSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, queryset=None):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(request.data['old_password']):
                return Response({"old_password": ["Wrong password"]}, status= status.HTTP_404_NOT_FOUND)
            self.object.set_password(request.data['new_password'])
            self.object.save()
            return Response({"message": "password updated"}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)