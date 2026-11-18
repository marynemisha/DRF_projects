from django.contrib.auth.models import User
from rest_framework import serializers
from Event.models import *

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# Event Serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDb
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDb
        fields = '__all__'
        read_only_fields = ['id', 'created_at','status']


# Event Member Serializer
class EventMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMemberDb
        fields = '__all__'
        read_only_fields = ['id', 'joined_at']