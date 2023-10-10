from .models import Category, Job, Candidate
from .serializers import CategorySerializer, JobSerializer, CandidateSerializer
from rest_framework import generics

# Category
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Job
class JobListCreate(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# Candidates
class CandidateListCreate(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class CandidateRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
