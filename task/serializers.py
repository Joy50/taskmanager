from rest_framework import serializers
from .models import Task, TaskPhoto

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPhoto
        fields = ('id', 'photo')

class TaskSerializer(serializers.ModelSerializer):
    photos = TaskPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'