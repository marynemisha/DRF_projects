from django.contrib.gis import serializers
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from tripmaster import serializers
from tripmaster.serializers import UserSerializer,TripSerializer
from tripmaster.models import TripDb
from rest_framework import authentication, permissions  
from tripmaster.permissions import OwnerOnly

# Create your views here.

class SignUpView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"message":"User created successfully"},status=201)
        return Response({"message":"Invalid data provided" },status=400)

class UserListView(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer_instance=UserSerializer(users,many=True)
        return Response(serializer_instance.data,status=200) 

class TripListCeateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        #qs=TripDb.objects.all()
        qs=TripDb.objects.filter(created_by=request.user)
        serializer_instance=TripSerializer(qs,many=True)
        return Response(data=serializer_instance.data)
     
    def post(self,request):
        form_data=request.data
        serializer_instance=TripSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={
                "Message":"Trip Created Successfully",
                "Trip Details":serializer_instance.data
            })
        else:
            return Response(data=serializer_instance.errors)    
            _
class TripRetrieveUpdateDeleteView(APIView): 
    authentication_classes=[authentication.BasicAuthentication]
    # permission_classes=[permissions.IsAuthenticated]
    permission_classes=[OwnerOnly]

    def get(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        if trip_object.created_by==request.user:
            serializer_instance=TripSerializer(trip_object)
            return Response(data=serializer_instance.data,status=200)
        else:
            return Response(data={
                "message":"No Access"
            }) 

    def put(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        #form_data=request.data
        #if trip_object.created_by==request.user:
        if trip_object.created_by!=request.user:
           # serializer_instance=TripSerializer(data=form_data,instance=trip_object)
           raise serializers.ValidationError("Access Denied")

        form_data=request.data
        serializer_instance=TripSerializer(data=form_data,instance=trip_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                    "Message":"Trip Updated Successfully",
                    "Updated details":serializer_instance.data
                })     
        else:
            return Response(data=serializer_instance.errors)    

        # else:
        #     return Response(data={
        #         "Message":"No Access"
        #     })    
        

    def delete(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        # form_data=request.data
        if trip_object.created_by==request.user:
            trip_object.delete()
            return Response(data={
                "Message":"Trip Deleted Successfully"

            })
        else:
            return Response(data={
                "Message":"No Changes"
            })