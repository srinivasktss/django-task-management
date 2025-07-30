from rest_framework.serializers import ModelSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Project

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
    
    def create(self, validated_data):
        try:
            project = Project(**validated_data)
            project.full_clean()
        except Exception as e:
            raise e
        return project
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.full_clean()
        instance.save()
        return instance

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']