from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from Expense.serializers import *
from Expense.models import *
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
class CategoryListCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        qs=CategoryDb.objects.filter(user=request.user)
        serializer_instance=CategorySerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=CategorySerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response({
                "Message":"Category added successfully..!",
                "Details":serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)
class CategoryRetrieveUpdateDelete(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,pk):
        category=get_object_or_404(CategoryDb,id=pk)
        if category.user==request.user:
            serializer_instance=CategorySerializer(category)
            return Response(data=serializer_instance.data)
        else:
            return Response({
                "Message":"No access..!"
            })
    def put(self,request,pk):
        category=get_object_or_404(CategoryDb,id=pk)
        if category.user!=request.user:
            return Response({
                "Message":"Access Denied"
            })
        form_data=request.data
        serializer_instance=CategorySerializer(data=form_data,instance=category)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message":"Updated..!",
                "Details":serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)
    def delete(self,request,pk):
        category=get_object_or_404(CategoryDb,id=pk)
        if category.user==request.user:
            category.delete()
            return Response({
                "Message":"Deleted"
            })
        else:
            return Response({
                "Message":"No access"
            })