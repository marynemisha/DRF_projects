from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from abroadstudy.serializers import *
from abroadstudy.models import *
from rest_framework import authentication,permissions,serializers
# Create your views here.
class Signupview(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message":"User created successfully...!"},status=201)
        return Response({"Message":"Invalid data"},status=400)

class Userview(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer_instance=UserSerializer(users,many=True)
        return Response(data=serializer_instance.data,status=200)


class CountryListCreateView(APIView):
    def get(self,request):
        qs=CountryDb.objects.all()
        serializer_instance=CountrySerializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=CountrySerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message":"Country added successfully..!",
                "Country Details":serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)

class CountryRetrieveUpdateDeleteView(APIView):
    def get(self, request, pk):
        country_object = get_object_or_404(CountryDb, id=pk)
        serializer_instance = CountrySerializer(country_object)
        return Response(data=serializer_instance.data)
    def put(self, request, pk):
        country_object = get_object_or_404(CountryDb, id=pk)
        form_data = request.data
        serializer_instance = CountrySerializer(data=form_data, instance=country_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Country updated successfully..!",
                "Updated details": serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)
    def delete(self, request, pk):
        country_object = get_object_or_404(CountryDb, id=pk)
        country_object.delete()
        return Response({
            "Message": "Country deleted successfully..!"
        })


class ApplicationListCreateView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        qs = ApplicationDb.objects.filter(applicant=request.user)
        serializer_instance = ApplicationSerializer(qs, many=True)
        return Response(data=serializer_instance.data)
    def post(self, request):
        form_data = request.data
        serializer_instance = ApplicationSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(applicant=request.user)
            return Response(data={
                "Message": "Application submitted successfully..!",
                "Application Details": serializer_instance.data
            }, status=201)
        else:
            return Response(data=serializer_instance.errors, status=400)

class ApplicationRetrieveUpdateDeleteView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        application_object = get_object_or_404(ApplicationDb, id=pk)
        if application_object.applicant == request.user:
            serializer_instance = ApplicationSerializer(application_object)
            return Response(data=serializer_instance.data)
        else:
            return Response({
                "Message": "You are not allowed to access this application...!"
            }, status=403)
    def put(self, request, pk):
        application_object = get_object_or_404(ApplicationDb, id=pk)
        if application_object.applicant == request.user:
            form_data = request.data
            serializer_instance = ApplicationSerializer(
                data=form_data, instance=application_object
            )
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response({
                    "Message": "Updated successfully..!",
                    "Updated details": serializer_instance.data
                })
            else:
                return Response(data=serializer_instance.errors, status=400)
        return Response({"Message": "Access Denied..!"}, status=403)
    def delete(self, request, pk):
        application_object = get_object_or_404(ApplicationDb, id=pk)
        if application_object.applicant == request.user:
            application_object.delete()
            return Response({"Message": "Deleted successfully..!"})
        return Response({"Message": "Access Denied..!"}, status=403)