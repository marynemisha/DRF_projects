from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from Event.serializers import *
from Event.models import *
from rest_framework import authentication,permissions
# Create your views here.
class SignUpView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"User created successfully..!"},status=201)
        return Response({"Message":"Invalid data"},status=400)
class UserListCreateView(APIView):
    def get(self,request):
        user=User.objects.all()
        serializer_instance=UserSerializer(user,many=True)
        return Response(data=serializer_instance.data)
class EventListCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        qs=EventDb.objects.filter(created_by=request.user)
        serializer_instance=EventSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=EventSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response({
                "Message":"Event created successfully..!",
                "Details":serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)
class EventRetrieveUpdateDelete(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,pk):
        event = get_object_or_404(EventDb,id=pk)
        if event.created_by == request.user:
            serializer_instance = EventSerializer(event)
            return Response(data=serializer_instance.data)
        return Response({
            "Message": "No access..!"
        }, status=403)
    def put(self,request,pk):
        event = get_object_or_404(EventDb,id=pk)
        if event.created_by != request.user:
            return Response({"Message": "Access Denied"},status=403)
        form_data = request.data
        serializer_instance = EventSerializer(data=form_data, instance=event)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Updated..!",
                "Details": serializer_instance.data
            })
        return Response(data=serializer_instance.errors,status=400)
    def delete(self,request,pk):
        event = get_object_or_404(EventDb,id=pk)
        if event.created_by == request.user:
            event.delete()
            return Response({"Message": "Deleted successfully..!"})
        return Response({"Message": "No access..!"},status=403)
class TaskListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        qs = TaskDb.objects.filter(event__created_by=request.user)
        serializer_instance = TaskSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data = request.data
        serializer_instance = TaskSerializer(data=form_data)
        if serializer_instance.is_valid():
            event = get_object_or_404(
                EventDb,
                id=form_data.get('event'),
                created_by=request.user
            )
            serializer_instance.save(event=event)
            return Response({
                "Message": "Task created successfully..!",
                "Details": serializer_instance.data
            }, status=201)
        return Response(data=serializer_instance.errors, status=400)
class TaskRetrieveUpdateDelete(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk):
        task = get_object_or_404(TaskDb, id=pk, event__created_by=request.user)
        serializer_instance = TaskSerializer(task)
        return Response(data=serializer_instance.data)
    def put(self,request,pk):
        task = get_object_or_404(
            TaskDb, id=pk, event__created_by=request.user)
        form_data = request.data
        serializer_instance = TaskSerializer(
            data=form_data, instance=task)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Task updated successfully..!",
                "Details": serializer_instance.data
            })
        return Response(data=serializer_instance.errors, status=400)
    def delete(self,request,pk):
        task = get_object_or_404(
            TaskDb, id=pk, event__created_by=request.user)
        task.delete()
        return Response({
            "Message": "Task deleted successfully..!"
        })
class EventMemberListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        qs = EventMemberDb.objects.filter(event__created_by=request.user)
        serializer_instance = EventMemberSerializer(qs, many=True)
        return Response(data=serializer_instance.data)
    def post(self, request):
        form_data = request.data
        serializer_instance = EventMemberSerializer(data=form_data)
        if serializer_instance.is_valid():
            event = get_object_or_404(
                EventDb,
                id=form_data.get('event'),
                created_by=request.user)
            serializer_instance.save(event=event)
            return Response({
                "Message": "Member added successfully..!",
                "Details": serializer_instance.data
            }, status=201)
        return Response(data=serializer_instance.errors, status=400)
class EventMemberRetrieveUpdateDelete(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk):
        member = get_object_or_404(
            EventMemberDb,
            id=pk,
            event__created_by=request.user)
        serializer_instance = EventMemberSerializer(member)
        return Response(data=serializer_instance.data)
    def put(self,request,pk):
        member = get_object_or_404(
            EventMemberDb,
            id=pk,
            event__created_by=request.user)
        form_data = request.data
        serializer_instance = EventMemberSerializer(
            data=form_data,
            instance=member)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Member updated successfully..!",
                "Details": serializer_instance.data
            })
        return Response(data=serializer_instance.errors, status=400)
    def delete(self,request,pk):
        member = get_object_or_404(
            EventMemberDb,
            id=pk,
            event__created_by=request.user)
        member.delete()
        return Response({
            "Message": "Member deleted successfully..!"
        })