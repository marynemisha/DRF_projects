from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from notes import serializers
from notes.serializers import *
from notes.models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
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
            serializer_instance.save(user=request.user)
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)

class Notesview(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        qs = get_object_or_404(NotesDb,id=pk,user=request.user)
        serializer_instance = NoteSerializer(qs)
        return Response(serializer_instance.data)
    def put(self,request,pk):
        note_object=get_object_or_404(NotesDb,id=pk)
        serializer_instance=NoteSerializer(data=request.data,instance=note_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data,status=200)
        return Response(data=serializer_instance.errors,status=400)
    def delete(self,request,pk):
        qs=get_object_or_404(NotesDb,id=pk)
        qs.delete()
        return Response({"Message":"Deleted Successfully!"})

class TaskView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        task=TaskDb.objects.filter(user=request.user)
        serializer_instance=TaskSerializer(task,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        serializer_instance=TaskSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)

class TaskRetrieveUpdateDeleteView(APIView):
    permission_classes=[IsAuthenticated]
    def get_task(self,request,id):
        return get_object_or_404(TaskDb,id=id,user=request.user)


    def get(self,request,id):
        task=self.get_task(request,id)
        serializer_instance=TaskSerializer(task)
        return Response(serializer_instance.data)
    def put(self,request,id):
        task=self.get_task(request,id)
        serializer_instance=TaskSerializer(task,data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data)
        return Response(serializer_instance.errors)
    def delete(self,request,id):
        task=self.get_task(request,id)
        task.delete()
        return Response(data={
            "Message":"Deleted...!"
        })


class JWT_Logout(APIView):
    def post(self,request):
        try:
            refresh_token=request.data.get("refresh")
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "Message":"Logout Success..!"
            })        
        except Exception:
            return Response({
                "Error":"Invalid refresh token...!"
            })