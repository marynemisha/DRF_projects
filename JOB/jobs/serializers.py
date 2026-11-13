from rest_framework import serializers
from jobs.models import JobDb, Applicant


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDb
        fields = '__all__'


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'