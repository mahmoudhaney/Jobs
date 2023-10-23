from rest_framework import serializers, validators
from .models import Category, Job, Application

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class CategoryJobsSerializer(serializers.ModelSerializer):
    jobs = JobSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('name', 'description', 'jobs')

class ApplicationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Application
        fields = ('name', 'email', 'website', 'cv', 'cover_letter', 'job', 'owner')
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Application.objects.all(),
                fields=['job', 'owner'],
                message=("You have already applied to this job"),
            )
        ]

class SpecificApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name', 'email', 'website', 'cv', 'cover_letter')
        extra_kwargs = {
        'job': {'read_only': True},
        } 

class JobApplicationsSerializer(serializers.ModelSerializer):
    applications = SpecificApplicationSerializer(many=True, read_only=True)
    class Meta:
        model = Job
        fields = ('title', 'description', 'job_type', 'applications')