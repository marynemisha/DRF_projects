from django.contrib.auth.models import User
from rest_framework import serializers
from abroadstudy.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model=CountryDb
        fields="__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDb
        fields = "__all__"
        read_only_fields=["applicant","application_status","applied date"]

