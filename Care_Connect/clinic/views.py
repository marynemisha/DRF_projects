from django.shortcuts import render,get_object_or_404
from clinic.models import DoctorDb,AppointmentDb
from clinic.serializers import Doctor_serializer,Appointment_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import time,timedelta,datetime
from rest_framework import serializers
# Create your views here.
class DoctorListCreateView(APIView):
    def get(self,request):
        qs=DoctorDb.objects.all()
        serializer_instance=Doctor_serializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=Doctor_serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class DoctorRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs=get_object_or_404(DoctorDb,id=pk)
        serializer_instance=Doctor_serializer(qs)
        return Response(data=serializer_instance.data)
    def put(self,request,pk):
        form_data=request.data
        doctor_object=get_object_or_404(DoctorDb,id=pk)
        serializer_instance=Doctor_serializer(data=form_data,instance=doctor_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
    def delete(self,request,pk):
        doctor_object=get_object_or_404(DoctorDb,id=pk)
        doctor_object.delete()
        return Response(data=
             {"message":"Deleted successfully..!"}
        )


class AppointmentListCreateView(APIView):
    def get(self,request):
        qs=AppointmentDb.objects.all()
        serializer_instance=Appointment_serializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data=request.data
        serializer_instance=Appointment_serializer(data=form_data)
        if serializer_instance.is_valid():
            print(serializer_instance.validated_data)
            appointment_date=serializer_instance.validated_data.get("appointment_date")
            doctor_id=serializer_instance.validated_data.get("doctor_id")
            last_appointment=AppointmentDb.objects.filter(
                appointment_date=appointment_date,
                doctor_id=doctor_id
            ).order_by("-token_number").first()

            if last_appointment is None:
                form_data["token_number"]=1
                form_data["appointment_time"]=time(10,0)
            else:
                form_data["token_number"]=last_appointment.token_number + 1
                current_time=datetime.combine(appointment_date,last_appointment.appointment_time)
                next_time=current_time+timedelta(minutes=15)


                #adding break time-lunch
                if next_time.time()==time(13,0):
                    next_time=datetime.combine(appointment_date,time(14,0))
                form_data["appointment_time"]=next_time.time()


                #adding slot completion time
                if next_time.time()==time(15,0):
                    raise serializers.ValidationError("No slot available today..")


            qs=AppointmentDb.objects.create(**form_data)
            serializer_instance=Appointment_serializer(qs)
            return Response(data=
                            {
                                "Message":"Booked successfully..!",
                                "Token Number is":form_data["token_number"],
                                "Appointmenr date is":form_data["appointment_date"],
                                "Appointment time is":form_data["appointment_time"]
                            })
        else:
            return Response(data=serializer_instance.errors)