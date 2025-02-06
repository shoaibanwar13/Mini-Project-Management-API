from rest_framework import serializers
from .models import User,Project,Task

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=('id','username','email','role','password')
class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")
    class Meta:
        model=Project
        fields = ["id", "title", "description", "creator"]
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields="__all__"

