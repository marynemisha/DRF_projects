from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Teamapp.models import *
from Teamapp.serializers import *
from Teamapp import serializers
from rest_framework import authentication,permissions
from rest_framework.exceptions import PermissionDenied
# Create your views here.
class Register(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=RegisterSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message":"User Created Successfully....!"
            })
        return Response({
            "Message":"Invalid data...!"
        })
class Userview(APIView):
    def get(self,request):
        user=User.objects.all()
        serializer_instance=RegisterSerializer(user,many=True)
        return Response(data=serializer_instance.data)
class ProjectCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        qs=ProjectDb.objects.filter(created_by=request.user)
        serializer_instance=ProjectSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=ProjectSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response({
                "Message":"Created successfully..!",
                "Details":serializer_instance.data
            })
        return Response(data=serializer_instance.errors)
class ProjectCRUDView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,pk):
        project=get_object_or_404(ProjectDb,id=pk)
        if project.created_by==request.user:
            serializer_instance=ProjectSerializer(project)
            return Response(data=serializer_instance.data)
        return Response({"Message":"No access...!"})
    def put(self,request,pk):
        project=get_object_or_404(ProjectDb,id=pk)
        if project.created_by!=request.user:
            raise serializers.ValidationError("Access Denied...!")
        form_data=request.data
        serializer_instance=ProjectSerializer(data=form_data,instance=project)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Updated successfully...!"})
        else:
            return Response(data=serializer_instance.errors)
    def delete(self,request,pk):
        project=get_object_or_404(ProjectDb,id=pk)
        if project.created_by==request.user:
            project.delete()
            return Response({
                "Message":"Deleted successfully...!"
            })
        else:
            return Response({
                "Message":"No changes...!"
            })

class ProjectMemberView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,pk):
        project=get_object_or_404(ProjectDb,id=pk)
        is_owner=project.created_by==request.user
        is_member=ProjectMemberDb.objects.filter(project=project,user=request.user).exists()
        if not(is_owner or is_member):
            raise PermissionDenied("You are not allowed to access this project...!")
        members=ProjectMemberDb.objects.filter(project=project)
        serializer_instance=ProjectMemberSerializer(members,many=True)
        return Response(data=serializer_instance.data,status=200)
    def post(self,request,pk):
        project=get_object_or_404(ProjectDb,id=pk)
        if project.created_by!=request.user:
            raise PermissionDenied("Only owner can add members..!")
        form_data=request.data
        serializer_instance=ProjectMemberSerializer(data=form_data,context={'project':project})
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message":"Added successfully...!"
            })
        else:
            return Response(data=serializer_instance.errors)

class ProjectMemberDeleteView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def delete(self,request,pk,id):
        project=get_object_or_404(ProjectDb,id=pk)
        if project.created_by!=request.user:
            raise PermissionDenied("Only owner can remove members..!")
        members=get_object_or_404(ProjectMemberDb,id=id,project=project)
        members.delete()
        return Response({
            "Message":"Deleted successfully..!"
        })