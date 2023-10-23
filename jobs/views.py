from .models import Category, Job, Application
from .serializers import CategorySerializer, CategoryJobsSerializer, JobSerializer, ApplicationSerializer, SpecificApplicationSerializer, JobApplicationsSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .permissions import IsAdminOrReadOnly, IsApplicationOwnerOrIsAdmin
from rest_framework.response import Response
from rest_framework import status

# Category
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

class ListCategoryJobs(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryJobsSerializer

# Job
class JobListCreate(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'job_type']
    search_fields = ['title']
    ordering_fields = ['title', 'experience', 'salary']

class JobRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

class ListJobApplications(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobApplicationsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

class RetrieveJobApplication(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = SpecificApplicationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)


# Application
class ApplicationListCreate(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsApplicationOwnerOrIsAdmin,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        try:
            applications = Application.objects.filter(owner=request.user.id)
            serializer = ApplicationSerializer(applications, many=True)
            return Response(serializer.data)
        except Application.DoesNotExist:
            return Response({'message': "No Application Yet"}, status= status.HTTP_404_NOT_FOUND)

class ApplicationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Override 'get', 'put', and 'delete' functions
    to use token auth instead of 'pk' for users
    and to filter the returned data
    """
    queryset = Application.objects.all()
    serializer_class = SpecificApplicationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsApplicationOwnerOrIsAdmin,)
    
    def get(self, request, job_id, *args, **kwargs):
        try:
            application = Application.objects.get(owner=request.user.id, job=job_id)
            serializer = SpecificApplicationSerializer(application)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({'detail': "Not found."}, status= status.HTTP_404_NOT_FOUND)

    def update(self, request, job_id, *args, **kwargs):
        try:
            application = Application.objects.get(owner=request.user.id, job=job_id)
            serializer = SpecificApplicationSerializer(application, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_200_OK)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Application.DoesNotExist:
            return Response({'detail': "Not found."}, status= status.HTTP_404_NOT_FOUND)

    def delete(self, request, job_id, *args, **kwargs):
        try:
            user = Application.objects.get(owner=request.user.id, job=job_id)
            user.delete()
            return Response(status= status.HTTP_204_NO_CONTENT)
        except Application.DoesNotExist:
            return Response({'detail': "Not found."}, status= status.HTTP_404_NOT_FOUND)
