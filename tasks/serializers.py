# tasks/serializers.py
from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserShortSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), required=False, source="assigned_to"
    )

    class Meta:
        model = Task
        fields = ("id","title","description","project","assigned_to","assigned_to_id","status","priority","due_date","created_by","created_at","updated_at")
        read_only_fields = ("created_by","created_at","updated_at","assigned_to")

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ("id","name","description","owner","tasks","created_at","updated_at")
        read_only_fields = ("owner","created_at","updated_at")
