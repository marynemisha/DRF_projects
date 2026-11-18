from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from notes import serializers
from notes.serializers import *
from notes.models import *
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class SignUpView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=RegisterSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message":"User created successfully"},status=201)
        return Response({"message":"Invalid data provided" },status=400)
class UserView(APIView):
    def get(self,request):
        qs=User.objects.all()
        serializer_instance=RegisterSerializer(qs,many=True)
        return Response(data=serializer_instance.data,status=201)

class NoteListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        notes=NotesDb.objects.filter(user=request.user)
        serializer_instance=NoteSerializer(notes,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        serializer_instance=NoteSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)