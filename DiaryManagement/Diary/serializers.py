from django.contrib.auth.models import User
from rest_framework import serializers
from Diary.models import *
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["id","username","email","password"]

    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model=DiaryDb
        fields="__all__"
        read_only_fields=["id","user","created_date"]