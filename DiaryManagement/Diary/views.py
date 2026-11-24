from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from Diary import serializers
from Diary.serializers import *
from Diary.models import *
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer_instance=RegisterSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Registered successfully..!"})
        return Response({"Message":"Invalid data"})
class UserView(APIView):
    def get(self,request):
        qs=User.objects.all()
        serializer_instance=RegisterSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
class DiaryView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        diary=DiaryDb.objects.filter(user=request.user)
        serializer_instance=DiarySerializer(diary,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        serializer_instance=DiarySerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)