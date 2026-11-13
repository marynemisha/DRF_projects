from django.shortcuts import render
from jobs.models import *
from jobs.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class JobListCreateView(APIView):
    def get(self, request):
        qs = JobDb.objects.all()
        serializer_instance = JobSerializer(qs, many=True)
        return Response(data=serializer_instance.data)
    def post(self, request):
        form_data = request.data
        serializer_instance = JobSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)
class ApplicantListCreateView(APIView):
    def get(self, request):
        qs = Applicant.objects.all()
        serializer_instance = ApplicantSerializer(qs, many=True)
        return Response(data=serializer_instance.data)
    def post(self, request):
        form_data = request.data
        serializer_instance = ApplicantSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

