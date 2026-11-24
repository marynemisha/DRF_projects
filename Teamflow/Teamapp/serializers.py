from django.contrib.auth.models import User
from rest_framework import serializers
from Teamapp.models import *

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["username","email","password"]
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProjectDb
        fields="__all__"
        read_only_fields=["id","created_by","created_at","updated_at"]


class ProjectMemberSerializer(serializers.ModelSerializer):
    username=serializers.CharField(write_only=True)
    member_username=serializers.CharField(source='user.username',read_only=True)
    member_user_id=serializers.IntegerField(source='user.id',read_only=True)

    class Meta:
        model=ProjectMemberDb
        fields=['id','username','member_username','member_user_id','joined_at']
        read_only_fields=['id','joined_at']


    def validate_username(self,value):
        try:
            user=User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("This user is not registered..!")
        project=self.context['project']
        if user==project.created_by:
            raise serializers.ValidationError("The creator is already the owner..!")
        if ProjectMemberDb.objects.filter(project=project,user=user).exists():
            raise serializers.ValidationError("The user is already a member..!")
        return value

    def create(self,validated_data):
        username=validated_data.pop('username')
        user=User.objects.get(username=username)
        project=self.context['project']
        return ProjectMemberDb.objects.create(project=project,user=user)

